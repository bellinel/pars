import asyncio
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from database.orm import get_site_id_olx, add_site_id_olx, update_site_id_olx


async def olx_parse():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-data-dir={tempfile.mkdtemp()}')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="135").install()), options=options)
    driver.get("https://www.olx.kz/nedvizhimost/prodazha-kvartiry/taldykorgan/?search%5Bfilter_enum_tipsobstvennosti%5D%5B0%5D=ot_hozyaina&search%5Bfilter_enum_tip_zhilya%5D%5B0%5D=vtorichnyy_rynok")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    # apartment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "listing-grid-container.css-d4ctjd")))
    apartment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-l9drzq")))
    name = apartment.find_element(By.CLASS_NAME, "css-1g61gc2").text
    price = apartment.find_element(By.CLASS_NAME, "css-uj7mm0").text.split(".")[0]
    card_id = apartment.get_attribute("id")
    
    current_id = await get_site_id_olx()
    
    if str(card_id) == str(current_id):
        print("ID совпадает OLX")
        return None
    url = apartment.find_element(By.CLASS_NAME, "css-u2ayx9").find_element(By.TAG_NAME, "a").get_attribute("href")
    result = f"{name}\n{price}\n{url}\n"
    await update_site_id_olx(int(card_id))
    driver.quit()
    print(result)
    return result
