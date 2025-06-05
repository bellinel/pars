import asyncio
import tempfile
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from database.orm import add_site_id_krisha, get_site_id_krisha, update_site_id_krisha

async def parse_krisha():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-data-dir={tempfile.mkdtemp()}')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="135").install()), options=options)
    # открываем сайт
    driver.get("https://krisha.kz/prodazha/kvartiry/taldykorgan/?das[who]=1")
    
    # ждем загрузки страницы
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    # находим секции с квартирами
    apartment = driver.find_element(By.CLASS_NAME, "a-list.a-search-list.a-list-with-favs").find_element(By.CSS_SELECTOR, "div.a-card")
    card_id = apartment.get_attribute("data-id")
    
    
    current_id = await get_site_id_krisha()
    
    if str(card_id) == str(current_id):
        print("ID совпадает KRISHA")
        return None
    try:
        apartment.find_element(By.CLASS_NAME, "label.label--yellow.label-user-owner")
    except:
        return None

    name = apartment.find_element(By.CLASS_NAME, "a-card__header-left").text
    # находим цену квартиры
    price = apartment.find_element(By.CLASS_NAME, "a-card__price").text
    # адрес квартиры
    address = apartment.find_element(By.CLASS_NAME, "a-card__subtitle").text
    # находим ссылку на квартиру
    link = apartment.find_element(By.CLASS_NAME, "a-card__header-left").find_element(By.TAG_NAME, "a").get_attribute("href")
    # выводим информацию о квартире
    result = f"{name}\n{price}\n{link}\n{address}\n"
    await update_site_id_krisha(int(card_id))
    driver.quit()
    return result




    
        
