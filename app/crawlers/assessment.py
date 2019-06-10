import re
import requests

from bs4 import BeautifulSoup

from config.components.crawler import (
    ASSESSMENT_LIST_PATH,
    ASSESSMENT_TA_PATH,
    ASSESSMENT_PATH,
    NOT_TIME_MESSAGE,
    DEFAULT_HEADERS,
)

from . import helper


CLASS_INFO_KEYS = ['open_class', 'class_no', 'class_name', 'teacher']
DETAIL_KEYS = [
    'Hide_Years',
    'Hide_Term',
    'Hide_OpClass',
    'Hide_Serial',
    'Hide_ClassShort',
    'Hide_TchNo',
    'Hide_TchName',
    'Hide_Cos_Name',
    'Hide_TermType',
    'Hide_SelStyle'
]


def get_assessments(cookies):
    res = requests.get(
        ASSESSMENT_LIST_PATH,
        cookies=cookies,
        headers=DEFAULT_HEADERS,
    )

    helper.check_response(res)

    if NOT_TIME_MESSAGE in res.text:
        return None

    soup = BeautifulSoup(res.text, 'html.parser')

    assessments = []
    columns = soup.select('#ASMList td table')[1:]  # 刪去標題列
    for rows in columns:
        class_info = [s.text.replace('\xa0', '') for s in rows.select('span')]
        detail_link = rows.select_one('a')

        detail_params = None
        if detail_link:
            p = re.compile('((?:\')([^\']*)(?:\'))')
            detail_params = [i[1] for i in p.findall(detail_link['onclick'])]

        class_info = dict(zip(CLASS_INFO_KEYS, class_info))
        class_info.update({'params': detail_params})
        assessments.append(class_info)

    return assessments


def fill_assessment(cookies, detail_params, score, suggestions):
    res = requests.get(
        ASSESSMENT_LIST_PATH,
        cookies=cookies,
        headers=DEFAULT_HEADERS,
    )
    helper.check_response(res)

    data = helper.get_data(res.text)
    data.update(dict(zip(DETAIL_KEYS, detail_params)))

    teacher_name = data['Hide_TchName']  # 存老師姓名回答 TA 時用

    target_path = ASSESSMENT_PATH
    if detail_params[-1] == '3':
        target_path = ASSESSMENT_TA_PATH

    res = requests.post(
        target_path,
        data=data,
        cookies=cookies,
        headers=DEFAULT_HEADERS,
    )
    helper.check_response(res)

    soup = BeautifulSoup(res.text, 'html.parser')
    question_numbers = [no['value'] for no in soup.select('[name=queNo]')]

    values = []
    for loop_count, i in enumerate(question_numbers):
        if detail_params[-1] == '3':
            if loop_count == 0:  # 知道有教學助理
                values.append('{}-1-'.format(i))
                continue

            if loop_count == 1:  # 處理教學助理姓名問題
                values.append('{}-1-{}'.format(i, teacher_name))
                continue

        choices = soup.select('[name=Radio{}]'.format(i))
        if len(choices) == 0:  # 如果單選找不到試試複選的
            choices = soup.select('[name=chk{}]'.format(i))
            choices.pop()  # 移除「其他請說明」選項
            values.extend(['{}-{}-'.format(i, c['value']) for c in choices])
            continue

        if detail_params[-1] == '3':
            choices.pop()  # 如果是 TA 的話，移除不適合請說明的選項

        if len(choices) < 5:  # 若長度不足 5 重複最後一個元素至長度 5
            last = choices[-1]
            choices.extend([last] * (5 - len(choices)))

        choices = choices[::-1]  # 反轉讓高分選項到最後面
        value = choices[score-1]['value']
        values.append('{}-{}-'.format(i, value))

    data = helper.get_data(res.text)
    data.update({'SaveData': 'Y', 'Hide_Str': ','.join(values)})

    areas = soup.select('[name=Areas]')
    if len(areas) > 0 and suggestions:
        area_value = areas[0]['value']
        data.update({'Hide_Str2': '{}<|>{}'.format(area_value, suggestions)})

    res = requests.post(
        target_path,
        data=data,
        cookies=cookies,
        headers=DEFAULT_HEADERS,
    )
    helper.check_response(res)
