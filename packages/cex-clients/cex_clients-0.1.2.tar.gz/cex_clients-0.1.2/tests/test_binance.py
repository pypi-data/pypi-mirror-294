from cex_clients.binance.web import Public


async def test_cur_filter():
    bn = Public()
    for cur in 'RUB', 'AZN', 'GEL':
        resp = await bn.get_pms_and_country_for_cur(cur)
        assert len(resp[0]) and len(resp[1]), "No data"
