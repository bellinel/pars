import asyncio
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import shutil

from database.orm import get_site_url_olx, update_site_url_olx


async def olx_parse():
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
    
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="135").install()), options=options)
        driver.get("https://www.olx.kz/nedvizhimost/prodazha-kvartiry/taldykorgan/?search%5Bfilter_enum_tipsobstvennosti%5D%5B0%5D=ot_hozyaina&search%5Bfilter_enum_tip_zhilya%5D%5B0%5D=vtorichnyy_rynok")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # apartment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "listing-grid-container.css-d4ctjd")))
        apartment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-cy='l-card']")))
        
    
            
        url = apartment.find_element(By.CLASS_NAME, "css-u2ayx9").find_element(By.TAG_NAME, "a").get_attribute("href")
        

        result = f"{url}"
        new_url = await update_site_url_olx(url)
        if new_url:
            return result
        else:
            return None

    except Exception:
        print("OLX ERROR")
        return None
    
    finally:
        if driver:
            driver.quit()
        
            
        
