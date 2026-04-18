import requests
from bs4 import BeautifulSoup
import csv
import os

def mine_product(model_no):
    # Robot headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Target URL: We search the specific model on Samsung India
    search_url = f"https://www.samsung.com/in/smartphones/all-smartphones/?search={model_no}"
    
    result = {
        "Model": model_no,
        "Brand": "Samsung",
        "Color": "N/A",
        "Attributes": "N/A",
        "Status": f"Not Found: {model_no}"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- MINING LOGIC ---
            # Note: Scrapers look for specific words in the page text
            page_text = soup.get_text().lower()
            
            # 1. Search for Color
            colors = ["Black", "White", "Silver", "Blue", "Gold", "Graphite", "Mint", "Yellow"]
            found_color = "N/A"
            for c in colors:
                if c.lower() in page_text:
                    found_color = c
                    break
            
            # 2. Search for common Attributes (RAM/Storage/Display)
            specs = []
            if "gb" in page_text: specs.append(re.search(r'\d+gb', page_text).group() if 're' in globals() else "Storage Found")
            if "5g" in page_text: specs.append("5G")
            if "display" in page_text: specs.append("Display Info Found")

            # --- STATUS CHECKPOINTS ---
            result["Color"] = found_color
            result["Attributes"] = ", ".join(specs) if specs else "N/A"

            # Determine Status
            if found_color != "N/A" and specs:
                result["Status"] = f"Found: {model_no}"
            elif found_color != "N/A" or specs:
                result["Status"] = f"Partial Found: {model_no}"
            else:
                # If the page loaded but no specific specs found
                result["Status"] = f"Not Found: {model_no}"

    except Exception as e:
        result["Status"] = f"Error: {model_no}"

    return result

if __name__ == "__main__":
    # Ensure models.txt exists
    if not os.path.exists('models.txt'):
        with open('models.txt', 'w') as f: f.write("")

    with open('models.txt', 'r') as f:
        models = f.read().splitlines()

    # Output to results.csv
    with open('results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Model", "Brand", "Color", "Attributes", "Status"])
        writer.writeheader()
        for m in models:
            if m.strip():
                print(f"Mining: {m}...")
                writer.writerow(mine_product(m.strip()))
