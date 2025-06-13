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
import shutil
from database.orm import add_site_id_krisha, get_site_id_krisha, update_site_id_krisha

async def parse_krisha():
    prefs = {"profile.managed_default_content_settings.images": 2}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--remote-debugging-port=0")
    options.add_experimental_option("prefs", prefs)
    

    # Запускаем Chrome
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(driver_version="135").install()),
            options=options
        )

        driver.get("https://krisha.kz/prodazha/kvartiry/taldykorgan/?das[who]=1")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        apartment = driver.find_element(
            By.CLASS_NAME, "a-list.a-search-list.a-list-with-favs"
        ).find_element(By.CSS_SELECTOR, "div.a-card")

        card_id = apartment.get_attribute("data-id")
        current_id = await get_site_id_krisha()

        if str(card_id) == str(current_id):
            print("ID совпадает KRISHA")
            return None

        try:
            apartment.find_element(
                By.CLASS_NAME, "label.label--yellow.label-user-owner"
            )
        except:
            print("Не от хозяина")
            return None

        
        link = apartment.find_element(By.CLASS_NAME, "a-card__header-left").find_element(
            By.TAG_NAME, "a"
        ).get_attribute("href")

        result = f"{link}"
        await update_site_id_krisha(int(card_id))
        
        return result

    finally:
        driver.quit()
      




    
        
