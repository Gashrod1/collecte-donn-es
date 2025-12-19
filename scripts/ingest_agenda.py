import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from datetime import datetime

BASE_URL = "https://www.bordeaux-tourisme.com"
URL = f"{BASE_URL}/agenda"
OUTPUT_DIR = "ingestion_data"

def scrape_agenda():
    print(f"Scraping {URL}...")
    headers = {
        "User-Agent": "Bot Etudiant - Contact: etudiant@example.com"
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch {URL}: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    # Based on analysis: class="ListSit-item js-list-sit-item" contains Card
    items = soup.find_all(class_="ListSit-item")
    
    data = []
    for item in items:
        try:
            card_title = item.find(class_="Card-title")
            title = card_title.get_text(strip=True) if card_title else "N/A"
            
            link_tag = item.find("a", href=True)
            link = link_tag["href"] if link_tag else ""
            if link and not link.startswith("http"):
                link = BASE_URL + link
            
            # Replace domain as requested
            link = link.replace("bordeaux-tourisme.com", "tourisme.example")
            
            card_label = item.find(class_="Card-label")
            date_info = card_label.get_text(strip=True) if card_label else "N/A"
            
            data.append({
                "title": title,
                "date_info": date_info,
                "link": link,
                "scraped_at": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error parsing item: {e}")
            continue
            
    if not data:
        print("No data found. Check selectors.")
        return

    df = pd.DataFrame(data)
    timestamp = int(time.time())
    filename = f"agenda_{timestamp}.parquet"
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    try:
        df.to_parquet(output_path)
        print(f"Saved {len(df)} items to {output_path}")
    except ImportError:
        print("Pyarrow not installed, saving to CSV instead.")
        csv_path = output_path.replace(".parquet", ".csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved {len(df)} items to {csv_path}")

if __name__ == "__main__":
    scrape_agenda()
