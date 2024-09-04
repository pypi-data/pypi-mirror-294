from urllib.parse import parse_qs
from pyrogram import Client
from pyrogram.raw import functions
from xync_schema.models import Agent

api_id = 20276309
api_hash = "077f4a2aa1debc0768c582c818d20f64"


async def get_init_data(agent: Agent):
    async with Client(agent.user_id, api_id, api_hash, session_string=agent.auth['sess']) as app:
        app: Client
        await app.send_message("me", "Greetings from **Pyrogram**!")
        bot = await app.resolve_peer('wallet')
        me = await app.resolve_peer(agent.user_id)
        res = await app.invoke(functions.messages.RequestWebView(peer=me, bot=bot, platform='chatparse'))
        raw = parse_qs(res.url)['tgWebAppUserId'][0].split('#tgWebAppData=')[1]
        j = parse_qs(raw)
        dct = {
          "web_view_init_data": {
            "query_id": j['query_id'][0],
            "user": j['user'][0],
            "auth_date": j['auth_date'][0],
            "hash": j['hash'][0]
          },
          "web_view_init_data_raw": raw,
          "ep": "menu"
        }
        return dct
