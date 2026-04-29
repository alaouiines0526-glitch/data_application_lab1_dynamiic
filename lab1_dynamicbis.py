from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd
import time

def scrape_producthunt_dynamic():
    # --- CONFIGURATION DU NAVIGATEUR ---
    chrome_options = Options()
    
    # On ajoute des arguments pour ne pas être détecté comme un robot
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # Mode Headless : Commente la ligne ci-dessous pour VOIR le navigateur s'ouvrir
    # chrome_options.add_argument("--headless") 
    
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.producthunt.com/search?q=mental+health+ai"
    
    products_data = [] # Notre "panier" pour stocker les produits trouvés

    try:
        print(f"Étape 1 : Connexion à {url}...")
        driver.get(url)
        
        # Étape 2 : Attente de sécurité pour que la page charge ses bases
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Étape 3 : Simulation de scroll (Le site est dynamique/infinite scroll)
        print("Étape 2 : Défilement de la page pour charger les produits...")
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(5) # On laisse 5 secondes pour que le JavaScript affiche les produits
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Étape 4 : Extraction des données
        # On utilise un sélecteur XPATH pour trouver tous les liens de produits
        items = driver.find_elements(By.XPATH, "//a[contains(@href, '/posts/')]")
        print(f"Nombre d'éléments détectés : {len(items)}")

        seen_names = set() # Pour éviter d'avoir deux fois le même produit
        for item in items:
            try:
                # get_attribute("textContent") est plus puissant que .text pour le contenu caché
                name = item.get_attribute("textContent").strip()
                
                # On vérifie que le nom n'est pas vide et pas déjà enregistré
                if name and len(name) > 2 and name not in seen_names:
                    products_data.append({
                        "name": name,
                        "source": "Product Hunt"
                    })
                    seen_names.add(name)
                    print(f"Produit capturé : {name}")
            except:
                continue

        # --- ÉTAPE 5 : SAUVEGARDES (LIVRABLES DU LAB) ---
        if products_data:
            # 1. Sauvegarde en format JSON (Données brutes)
            with open('raw_data.json', 'w', encoding='utf-8') as f:
                json.dump(products_data, f, indent=4, ensure_ascii=False)

            # 2. Sauvegarde en format CSV (Tableau Pandas)
            df = pd.DataFrame(products_data)
            df.to_csv('product_hunt_results.csv', index=False, encoding='utf-8')
            
            print("-" * 30)
            print("BRAVO : L'extraction est réussie !")
            print(f"Fichiers créés : raw_data.json et product_hunt_results.csv ({len(df)} lignes)")
        else:
            print("ERREUR : Aucun produit trouvé. Vérifie la fenêtre Chrome (Captcha ?)")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")

    finally:
        # Étape 6 : On ferme toujours le navigateur à la fin
        driver.quit()

# Lancement du programme
if __name__ == "__main__":
    scrape_producthunt_dynamic()