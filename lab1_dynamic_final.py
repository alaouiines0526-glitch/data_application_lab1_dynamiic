import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def lab1_dynamic_final():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    all_products_raw = []
    seen_names = set()
    current_page = 1

    try:
        driver.get("https://www.producthunt.com/search?q=mental+health+ai")
        wait = WebDriverWait(driver, 20)

        while True:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(5) 

            items = driver.find_elements(By.XPATH, "//a[contains(@href, '/posts/')]")
            
            page_data = []
            for item in items:
                try:
                    name = item.get_attribute("textContent").strip()
                    if name and len(name) > 2 and name not in seen_names:
                        product_entry = {
                            "id": len(all_products_raw) + 1,
                            "name": name,
                            "page": current_page,
                            "timestamp": time.time()
                        }
                        all_products_raw.append(product_entry)
                        page_data.append(product_entry)
                        seen_names.add(name)
                except:
                    continue

            with open('raw_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_products_raw, f, indent=4, ensure_ascii=False)

            try:
                next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Load more')] | //a[contains(text(), 'Next')]")
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(2)
                next_button.click()
                current_page += 1
                time.sleep(5)
            except:
                break

        if all_products_raw:
            df = pd.DataFrame(all_products_raw)
            df.to_csv('product_hunt_final.csv', index=False, encoding='utf-8')

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    lab1_dynamic_final()