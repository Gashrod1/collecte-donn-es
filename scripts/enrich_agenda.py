import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import glob

OUTPUT_DIR = "ingestion_data"

def get_latest_file():
    # Support both parquet and csv in case parquet failed
    files = glob.glob(os.path.join(OUTPUT_DIR, "agenda_*"))
    # Filter out enriched files to avoid loop
    files = [f for f in files if "enriched" not in f]
    if not files:
        return None
    return max(files, key=os.path.getctime)

def enrich_data():
    input_file = get_latest_file()
    if not input_file:
        print("No input file found.")
        return

    print(f"Reading from {input_file}...")
    if input_file.endswith(".parquet"):
        df = pd.read_parquet(input_file)
    else:
        df = pd.read_csv(input_file)
    
    details = []
    headers = {
        "User-Agent": "Bot Etudiant - Contact: etudiant@example.com"
    }
    
    # Limit to first 5 for demo/safety
    print("Enriching first 5 items...")
    for index, row in df.head(5).iterrows():
        link = row["link"]
        # Revert domain for scraping
        scrape_link = link.replace("tourisme.example", "bordeaux-tourisme.com")
        
        print(f"Scraping details for {scrape_link}...")
        try:
            time.sleep(1) # Rate limiting
            response = requests.get(scrape_link, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                # Try to find description
                # Looking for meta description as a safe fallback
                description = ""
                meta_desc = soup.find("meta", attrs={"name": "description"})
                if meta_desc:
                    description = meta_desc.get("content", "")
                else:
                    # Fallback to first paragraph of body
                    p = soup.find("p")
                    description = p.get_text(strip=True) if p else "No description found"
                
                details.append(description)
            else:
                details.append(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
            details.append(str(e))
    
    # Pad the rest with None if we only did 5
    details += [None] * (len(df) - len(details))
            
    df["description"] = details
    
    timestamp = int(time.time())
    output_path = os.path.join(OUTPUT_DIR, f"agenda_enriched_{timestamp}.parquet")
    
    try:
        df.to_parquet(output_path)
        print(f"Saved enriched data to {output_path}")
    except ImportError:
        csv_path = output_path.replace(".parquet", ".csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved enriched data to {csv_path}")

if __name__ == "__main__":
    enrich_data()
