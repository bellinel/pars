import asyncio

from database.engine import Database
from olx import olx_parse
from krisha import parse_krisha
from send_message import send_whatsapp_message



db = Database()




async def send_message_and_parse_krisha():
    try:
        krisha = await parse_krisha()
        if krisha:
            print("Krisha:", krisha)
            await send_whatsapp_message(text=krisha)
    except Exception as e:
        print("Ошибка в krisha:", e)

async def send_message_and_parse_olx():
    try:
        olx = await olx_parse()
        if olx:
            print("OLX:", olx)
            await send_whatsapp_message(text=olx)
    except Exception as e:
        print("Ошибка в olx:", e)

async def main():
    await db.init()  # Один раз

    while True:
        # Запуск задач параллельно
        task_krisha = asyncio.create_task(send_message_and_parse_krisha())
        task_olx = asyncio.create_task(send_message_and_parse_olx())

        # Ждём обе
        await asyncio.gather(task_krisha, task_olx)

        # Интервал перед следующим запуском
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
