import requests

from config.components.crawler import (
    LOGIN_PATH,
    INDEX_PATH,
    LOGIN_ERROR_MESSAGE,
)

from . import helper


def login(username, password):
    client = requests.Session()
    res = client.get(LOGIN_PATH)
    helper.check_response(res)

    data = helper.get_data(res.text)
    data.update({'UserID': username, 'PWD': password})

    res = client.post(LOGIN_PATH, data)
    helper.check_response(res)

    if res.url == INDEX_PATH:
        return True, dict(client.cookies)

    return False, None


def check_login(cookies):
    res = requests.get(INDEX_PATH, cookies=cookies)
    helper.check_response(res)
    return LOGIN_ERROR_MESSAGE not in res.text
