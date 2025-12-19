import requests
import pandas as pd
import os
from datetime import datetime
import io

# Configuration
OUTPUT_DIR = "ingestion_data"
DATE_STR = datetime.now().strftime("%Y%m%d")

# URLs
URLS = {
    "traffic": "https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/ci_trafi_l/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B",
    "school_holidays": "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-calendrier-scolaire/exports/csv",
    "public_holidays": "https://www.data.gouv.fr/api/1/datasets/r/6637991e-c4d8-4cd6-854e-ce33c5ab49d5",
    "weather": "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/donnees-synop-essentielles-omm/exports/csv?refine=nom:BORDEAUX-MERIGNAC"
}

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def fetch_and_save(key, url, delimiter=";"):
    print(f"[{key}] Fetching data from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Read CSV content
        # Some APIs return ; separated, others ,
        # We try to detect or use the provided delimiter
        content = response.content
        
        try:
            df = pd.read_csv(io.BytesIO(content), sep=delimiter)
        except:
            # Fallback to comma if semicolon fails
            print(f"[{key}] Failed with delimiter '{delimiter}', trying ','")
            df = pd.read_csv(io.BytesIO(content), sep=",")
            
        print(f"[{key}] Data shape: {df.shape}")
        
        # Save to Parquet
        filename = f"{key}_{DATE_STR}.parquet"
        filepath = os.path.join(OUTPUT_DIR, filename)
        df.to_parquet(filepath, index=False)
        print(f"[{key}] Saved to {filepath}")
        
    except Exception as e:
        print(f"[{key}] Error: {e}")

def main():
    ensure_output_dir()
    
    # Traffic (Bordeaux Metropole usually uses ';')
    fetch_and_save("traffic", URLS["traffic"], delimiter=";")
    
    # School Holidays (Education gouv usually ';')
    fetch_and_save("school_holidays", URLS["school_holidays"], delimiter=";")
    
    # Public Holidays (data.gouv.fr often ',')
    fetch_and_save("public_holidays", URLS["public_holidays"], delimiter=",")
    
    # Weather (OpenDataSoft usually ';')
    fetch_and_save("weather", URLS["weather"], delimiter=";")

if __name__ == "__main__":
    main()
