import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_product_hunt_1_3():
    # Configuration initiale de Selenium
    chrome_options = Options()
    # Note : Le mode headless est désactivé par défaut pour faciliter le débugging
    # chrome_options.add_argument("--headless") 
    
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.producthunt.com/search?q=mental+health+ai"
    
    try:
        print(f"Ouverture du navigateur sur : {url}")
        driver.get(url)
        
        # 1. Stratégie d'attente (Waiting Strategy)
        # On attend que le corps de la page soit chargé
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Simulation d'un scroll pour déclencher le chargement des données JS[cite: 1]
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(4) 

        # 2. Localisation des éléments (Location Strategies)[cite: 1]
        # Utilisation d'un sélecteur XPath flexible pour capturer les blocs de produits
        items = driver.find_elements(By.XPATH, "//div[contains(@class, 'styles_item')] | //a[contains(@data-test, 'post-item')]")
        
        raw_data = []
        
        for index, item in enumerate(items[:15]): # On limite aux premiers résultats
            try:
                # Gestion des exceptions par point de donnée[cite: 1]
                text_content = item.text.split('\n')
                if len(text_content) >= 2:
                    product_info = {
                        "id": index + 1,
                        "name": text_content[0],
                        "tagline": text_content[1],
                        "votes": text_content[-1] if '▲' in text_content[-1] else "N/A"
                    }
                    raw_data.append(product_info)
            except Exception as e:
                print(f"Erreur d'extraction sur l'item {index} : {e}")

        # 3. Stockage intermédiaire en JSON (Exigence 1.3.1)[cite: 1]
        with open("product_hunt_raw.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=4, ensure_ascii=False)
        
        # 4. Structuration finale en CSV (Exigence 1.3.2)[cite: 1]
        df = pd.DataFrame(raw_data)
        df.to_csv("product_hunt_final.csv", index=False)
        
        print(f"Succès : {len(raw_data)} produits extraits.")
        print("Fichiers 'product_hunt_raw.json' et 'product_hunt_final.csv' créés.")

    except Exception as global_error:
        print(f"Une erreur critique est survenue : {global_error}")
    finally:
        # Toujours fermer le driver (Best practice mentionnée dans le Lab)[cite: 1]
        driver.quit()

if __name__ == "__main__":
    scrape_product_hunt_1_3()