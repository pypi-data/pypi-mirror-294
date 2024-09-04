from json import loads
from http_client import Client, repeat_on_fault

from cex_clients.loader import HT


class Public(Client):
    base_url = 'https://www.htx.com'
    middle_url = '/-/x'

    # 1: Get all: currency,pay,allCountry,coin
    @repeat_on_fault()
    async def get_all(self) -> (dict, dict, dict, dict):
        res = await self.get('/otc/v1/data/config-list?type=currency,pay,allCountry,coin')
        return res['data'].values()


class Earn(Client):
    base_url = 'https://www.htx.com'
    middle_url = '/-/x/hbg/'

    # 1: Get BETH staking details
    @repeat_on_fault()
    async def get_staking_products(self):
        res = await self.get('v1/hbps/vote/product/list')
        return res['data']

    # 2: Get ongoing earn products
    @repeat_on_fault()
    async def get_recommend_products(self):
        res = await self.get('v1/saving/mining/prime_earn/activity/onGoing')
        return res['data']

    # 3: Get newList earn products
    @repeat_on_fault()
    async def get_new_products(self, page: int = 1):
        res = (await self.get('v4/saving/mining/project/queryLimitList', {'page': page}))['data']
        if len(res) == 6:
            res += await self.get_new_products(page+1)
        return res

    # 4: Get fixed earn products
    @repeat_on_fault()
    async def get_lock_products(self, page: int = 1):
        res = (await self.get('v4/saving/mining/project/queryFixedList', {'page': page}))['data']
        if len(res) == 6:
            res += await self.get_lock_products(page+1)
        return res

    # 5: Get flexible earn products
    @repeat_on_fault()
    async def get_flex_products(self, page: int = 1):
        res = (await self.get('v4/saving/mining/project/queryYbbList', {'page': page}))['data']
        if len(res) == 10:
            res += await self.get_flex_products(page+1)
        return res

    # 6: Get ongoing earn products
    @repeat_on_fault()
    async def get_large_products(self):
        res = await self.get('v4/saving/mining/project/largeAmtList')
        return res['data']


class Private(Client):  # Huobi async client
    base_url = 'https://www.htx.com'
    middle_url = '/'
    headers = loads(HT)

    """ PUBLIC METHS """
    # 1: Get BETH staking details
    @repeat_on_fault()
    async def get_beth_rate(self):
        # pool token required
        res = await self.get('hbp/eth2/v1/staking/eth2/profit')
        return res['data']['mr']
