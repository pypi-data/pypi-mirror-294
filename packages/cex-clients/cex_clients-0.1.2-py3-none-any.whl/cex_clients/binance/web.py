from http_client import Client


class BinanceClient(Client):
    base_url = 'https://p2p.binance.com'


class Public(BinanceClient):
    middle_url = '/bapi/c2c/v2/public/c2c/'

    async def get_pms_and_country_for_cur(self, cur: str) -> ([str], [str]):
        data = {"fiat": cur, "classifies": ["mass", "profession"]}
        res = await self.post('adv/filter-conditions', data)
        return [(r['identifier'], r['id'], r['tradeMethodName'])  for r in res['data']['tradeMethods']], [r['scode'] for r in res['data']['countries'] if r['scode']!='ALL']  # countries,tradeMethods,periods


# class Private(Public): # todo: base class: Public or Client?
class Private(BinanceClient):
    # auth: dict =
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'Content-Type': 'application/json',
        'clienttype': 'web',
    }

    def seq_headers(self):
        return {
            'csrftoken': self.auth['tok'],
            'cookie': f'p20t=web.{self.id}.{self.auth["cook"]}',
        }
