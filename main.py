import asyncio

from database.engine import Database
from olx import olx_parse
from krisha import parse_krisha
from send_message import send_whatsapp_message
from database.orm import clear_olx_table



db = Database()





async def periodic_clear():
    while True:
        await clear_olx_table()
        await asyncio.sleep(24 * 60 * 60)


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
    await db.init()
    print("База данных инициализирована")
    asyncio.create_task(periodic_clear())
    while True:
        # Запуск задач параллельно
        await send_message_and_parse_krisha()
        await asyncio.sleep(5)
        await send_message_and_parse_olx()
        await asyncio.sleep(5)

        # Ждём обе
        

        # Интервал перед следующим запуском
        

if __name__ == "__main__":
    asyncio.run(main())
