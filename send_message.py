import os
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

IDISTANSE = os.getenv("IDISTANSE")
API_KEY = os.getenv("API_KEY")
GROUP_ID = os.getenv("GROUP_ID")


async def send_whatsapp_message(text):
    url = f"https://7105.api.greenapi.com/waInstance{IDISTANSE}/sendMessage/{API_KEY}"
    

    payload = {
        
        'chatId': GROUP_ID,
        "message": f'{text}'
    }

    headers = {
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response_text = await response.text()
            print(response_text)


# asyncio.run(send_whatsapp_message("test"))






