import requests

# Path
HOST = 'http://ntcbadm.ntub.edu.tw'
LOGIN_PATH = HOST + '/login.aspx'
INDEX_PATH = HOST + '/Portal/indexSTD.aspx'
ASSESSMENT_LIST_PATH = HOST + '/STDWEB/Assessment_Main.aspx'
ASSESSMENT_PATH = HOST + '/STDWEB/Assessment_Detail.aspx'
ASSESSMENT_TA_PATH = HOST + '/STDWEB/Assessment_Detail_TA.aspx'  # 教學助理

# Message
NOT_TIME_MESSAGE = '目前非期末教學評量時間'
LOGIN_ERROR_MESSAGE = '閒置過久或尚未登入系統，請重新登入系統!'

# Requests config
requests.adapters.DEFAULT_RETRIES = 5  # 增加重試次數，避免連線失效

# Headers
DEFAULT_HEADERS = {
    'Connection': 'close',
}
