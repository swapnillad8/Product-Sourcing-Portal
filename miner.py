import requests
from bs4 import BeautifulSoup
import csv
import re
import os

def mine_sku(model):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    # Targeted search for your specific model
    url = f"https://www.google.com/search?q=Samsung+India+{model}+specs"
    
    result = {"Model": model, "Color": "N/A", "Attributes": "N/A", "Status": f"Not Found: {model}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()

        # 1. Mining Color
        colors = ["Spotlight Blue", "Black", "White", "Silver", "Mint", "Graphite"]
        for c in colors:
            if c.lower() in text:
                result["Color"] = c
                break

        # 2. Mining Attributes (Storage/Display/Capacity)
        attrs = []
        if "gb" in text: attrs.append(re.search(r'\d+gb', text).group().upper())
        if "inch" in text or "display" in text: attrs.append("Display Found")
        if "kg" in text: attrs.append(re.search(r'\d+kg', text).group())
        
        result["Attributes"] = ", ".join(attrs) if attrs else "N/A"

        # 3. Setting Status
        if result["Color"] != "N/A" and result["Attributes"] != "N/A":
            result["Status"] = f"Found: {model}"
        elif result["Color"] != "N/A" or result["Attributes"] != "N/A":
            result["Status"] = f"Partial Found: {model}"
            
    except Exception:
        result["Status"] = f"Error: {model}"
        
    return result

if __name__ == "__main__":
    if os.path.exists('models.txt'):
        with open('models.txt', 'r') as f:
            models = [line.strip() for line in f if line.strip()]
        
        with open('results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Model", "Color", "Attributes", "Status"])
            writer.writeheader()
            for m in models:
                writer.writerow(mine_sku(m))
