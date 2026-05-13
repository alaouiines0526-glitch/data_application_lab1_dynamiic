import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def lab1_2_static_scraping():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    all_repos = []
    base_url = "https://github.com/search?q=mental+health+ai&type=repositories"

    for page in range(1, 6):
        url = f"{base_url}&p={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        repos = soup.select('div.f4.text-normal') or soup.select('div.search-title')
        
        for repo in repos:
            name_tag = repo.find('a')
            if name_tag:
                repo_data = {
                    "repo_name": name_tag.get_text(strip=True),
                    "url": "https://github.com" + name_tag['href'],
                    "page": page
                }
                all_repos.append(repo_data)
        
        time.sleep(2)

    if all_repos:
        df = pd.DataFrame(all_repos)
        df.to_csv('github_static_results.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    lab1_2_static_scraping()