from bs4 import BeautifulSoup


def get_data(page):
    soup = BeautifulSoup(page, 'html.parser')

    data = {}
    for field in soup.find_all('input'):
        if not field.get('name'):
            continue

        data[field['name']] = field.get('value') or ''

    return data


def check_response(response):
    if not response.ok:
        raise Exception('Request error with {}'.format(response.status_code))
