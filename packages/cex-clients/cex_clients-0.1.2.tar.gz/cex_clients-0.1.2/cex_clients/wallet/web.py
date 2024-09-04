from aiohttp import ClientResponse
from aiohttp.http_exceptions import HttpProcessingError
from http_client import Client, repeat_on_fault
from xync_schema.models import Agent

from cex_clients.wallet.pyro import get_init_data


class Private(Client):
    base_url = 'https://walletbot.me'
    middle_url = '/'
    headers = {'Content-Type': 'application/json'}
    agent: Agent
    tok: str = None
    jwt: str = None

    def __init__(self, agent: Agent):
        self.agent = agent
        super().__init__()

    # 1: Get JWT
    async def get_token(self, agent: Agent) -> dict:
        init_data = await get_init_data(agent)
        tokens = await self.post('api/v1/users/auth/', init_data)
        self.tok = tokens['value']
        self.jwt = tokens['jwt']
        self.headers['Wallet-Authorization'] = self.jwt
        self.headers['Authorization'] = 'Bearer ' + self.tok
        await self.close()
        super().__init__()
        return tokens

    async def proc(self, resp: ClientResponse) -> dict | str:
        try:
            return await super().proc(resp)
        except HttpProcessingError as e:
            if e.code == 401:
                await self.get_token(self.agent)
                raise Exception

    # 2: Get Status
    async def get_status(self) -> dict:
        status = await self.get('users/public-api/v2/region-verification/status/')
        return status

    # 3: Get Transaction
    async def get_transactions(self, limit: int = 20) -> dict:
        transactions = await self.get('api/v1/transactions/', params={'limit': limit}, headers={'Authorization': self.tok})
        return transactions

    # 4: Get Campaigns
    async def get_campaigns(self) -> dict:
        campaigns = await self.get('v2api/earn/campaigns/')
        return campaigns

    # 5: Get Ads

    @repeat_on_fault(2)
    async def get_ads(self, coin: str = "TON", cur: str = "RUB", tt: str = "SALE", offset: int = 0, limit: int = 100) -> dict:
        params = {"baseCurrencyCode":coin,"quoteCurrencyCode":cur,"offerType":tt,"offset":offset,"limit":limit}  # ,"merchantVerified":"TRUSTED"
        ads = await self.post('p2p/public-api/v2/offer/depth-of-market/', params)
        return ads


# async def main():
#     c = Private()
#     await c.get_token()
