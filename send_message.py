import aiohttp
import asyncio

async def send_whatsapp_message(text):
    # url = "https://7105.api.greenapi.com/waInstance7105255577/sendMessage/259b7a7d620742d1babbe846294245907c353e7490eb46d5b3"
    url = "https://7105.api.greenapi.com/waInstance7105218511/sendMessage/fb4cbfa4f35d4141b208cf56b8da429680dc269c41464b3b97"

    payload = {
        "chatId": "120363399527013430@g.us",
        # 'chatId': '375257224153@c.us',
        "message": f'{text}'
    }

    headers = {
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response_text = await response.text()
            print(response_text)




asyncio.run(send_whatsapp_message("test"))




