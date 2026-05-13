import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def lab2_driver_management():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.producthunt.com/")
        
        products = []
        items = driver.find_elements(By.CSS_SELECTOR, "[data-test*='post-name']")
        
        for item in items:
            name = item.get_attribute("textContent").strip()
            if name:
                products.append({"name": name})

        if products:
            with open('data_lab2.json', 'w', encoding='utf-8') as f:
                json.dump(products, f, indent=4, ensure_ascii=False)
            
            pd.DataFrame(products).to_csv('data_lab2.csv', index=False)

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    lab2_driver_management()