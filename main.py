import asyncio
import os
from datetime import datetime, timedelta

from database.engine import Database
from olx import olx_parse, create_olx_driver
from krisha import parse_krisha, create_krisha_driver
from send_message import send_whatsapp_message
from database.orm import clear_olx_table

db = Database()

LAST_CLEAR_FILE = "last_clear.txt"  # просто файл в текущей папке
CLEAR_INTERVAL = timedelta(hours=24)


def read_last_clear_time():
    if not os.path.exists(LAST_CLEAR_FILE):
        return None
    try:
        with open(LAST_CLEAR_FILE, "r") as f:
            content = f.read().strip()
            return datetime.fromisoformat(content)
    except Exception:
        return None


def write_last_clear_time(dt: datetime):
    with open(LAST_CLEAR_FILE, "w") as f:
        f.write(dt.isoformat())


async def periodic_clear():
    while True:
        last_clear = read_last_clear_time()
        now = datetime.now()
        if not last_clear or (now - last_clear) >= CLEAR_INTERVAL:
            print(f"Очистка базы в {now.isoformat()}")
            await clear_olx_table()
            write_last_clear_time(now)

        else:
            remaining = CLEAR_INTERVAL - (now - last_clear)
            print(f"Очистка не требуется, следующий запуск через {remaining}")
        await asyncio.sleep(60)  # Проверяем каждую минуту


async def send_message_and_parse_krisha(driver):
    try:
        krisha = await parse_krisha(driver)
        if krisha:
            print("Krisha:", krisha)
            await send_whatsapp_message(text=krisha)
    except Exception as e:
        print("Ошибка в krisha:", e)


async def send_message_and_parse_olx(driver):
    try:
        olx = await olx_parse(driver)
        if olx:
            print("OLX:", olx)
            await send_whatsapp_message(text=olx)
            
    except Exception as e:
        print("Ошибка в olx:", e)







from selenium.common.exceptions import WebDriverException


async def main_loop():
    while True:
        try:
            await db.init()
            print("База данных инициализирована")

            krisha_driver = create_krisha_driver()
            olx_driver = create_olx_driver()

            asyncio.create_task(periodic_clear())

            try:
                while True:
                    try:
                        await send_message_and_parse_krisha(krisha_driver)
                        await asyncio.sleep(5)
                        await send_message_and_parse_olx(olx_driver)
                        await asyncio.sleep(5)

                    except WebDriverException as e:
                        print(f"Ошибка в WebDriver: {e}")
                        # Можно перезапустить драйверы, если надо
                        break

                    except Exception as e:
                        print(f"Ошибка в основном цикле: {e}")
                        print("Перезапуск цикла через 5 секунд...")
                        await asyncio.sleep(5)

            finally:
                print("Закрываю драйверы...")
                try:
                    krisha_driver.quit()
                except Exception:
                    pass
                try:
                    olx_driver.quit()
                except Exception:
                    pass

        except Exception as e:
            print(f"Критическая ошибка в main_loop: {e}")
            print("Перезапуск всего процесса через 5 секунд...")
            await asyncio.sleep(5)








if __name__ == "__main__":
    asyncio.run(main_loop())
