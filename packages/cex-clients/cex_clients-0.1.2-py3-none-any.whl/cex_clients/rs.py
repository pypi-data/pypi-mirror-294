from http.client import HTTPSConnection
from json import dumps, loads


class RsClient:
    host: str
    cn: HTTPSConnection
    headers = {
        "accept": "application/json",
        "cookie": ";",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    def __init__(self, host: str = None, headers: dict = None):
        if host:
            self.host = host
        if headers:
            self.headers.update(headers)
        self.cn = HTTPSConnection(self.host, timeout=15)

    def get(self, url, headers: dict = None) -> dict:
        self.cn.request("GET", url, headers={**self.headers, **(headers or {})})
        return self._resp()

    def post(self, url, json: dict = None, headers: dict = None) -> dict:
        if json:
            json = dumps(json)
        self.cn.request("POST", url, json, {**self.headers, **(headers or {})})
        return self._resp()

    def _resp(self) -> dict:
        resp = self.cn.getresponse().read()
        return loads(resp)

    def close(self):
        self.cn.close()
