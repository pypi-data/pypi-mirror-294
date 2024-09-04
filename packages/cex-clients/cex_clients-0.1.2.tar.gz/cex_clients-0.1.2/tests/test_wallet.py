from tortoise_api_model import init_db
from xync_schema import models
from xync_schema.models import Agent

from cex_clients.loader import DSN
from cex_clients.wallet.web import Private


async def test_cur_filter():
    await init_db(DSN, models)
    agent = await Agent[1]
    tg = Private(agent)
    for cur in 'RUB', 'AZN', 'GEL':
        for coin in 'TON', 'USDT', 'BTC':
            for tt in 'SALE', 'PURCHASE':
                ads = await tg.get_ads(coin, cur, tt)
                assert len(ads), "No data"
