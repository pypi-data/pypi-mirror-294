from http_client import Client


class Public(Client):
    base_url = 'https://www.okx.com'
    middle_url = '/v2/'
