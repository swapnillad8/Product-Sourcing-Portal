import requests
from bs4 import BeautifulSoup
import csv
import os
import re

def mine_product(model_no):
    # Professional headers to prevent being blocked by PHP/Java servers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    # We use a broad search query to find the specific product page
    search_url = f"https://www.google.com/search?q=Samsung+India+{model_no}+specifications"
    
    result = {
        "Model": model_no,
        "Brand": "Samsung",
        "Color": "N/A",
        "Attributes": "N/A",
        "Status": f"Not Found: {model_no}"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().lower()

        # --- KEYWORD DETECTION ---
        # 1. Color Detection
        colors = ["Spotlight Blue", "Black", "White", "Silver", "Graphite", "Gold", "Mint"]
        found_color = "N/A"
        for c in colors:
            if c.lower() in page_text:
                found_color = c
                break
        
        # 2. Spec Detection (Storage, 5G, Display)
        specs = []
        if "gb" in page_text:
            storage = re.findall(r'\d+gb', page_text)
            if storage: specs.append(storage[0].upper())
        if "5g" in page_text: specs.append("5G")
        if "display" in page_text or "inch" in page_text: specs.append("Display Identified")

        # --- STATUS LOGIC ---
        result["Color"] = found_color
        result["Attributes"] = ", ".join(specs) if specs else "N/A"

        if found_color != "N/A" and specs:
            result["Status"] = f"Found: {model_no}"
        elif found_color != "N/A" or specs:
            result["Status"] = f"Partial Found: {model_no}"
        else:
            result["Status"] = f"Not Found: {model_no}"

    except Exception:
        result["Status"] = f"Error: {model_no}"

    return result

if __name__ == "__main__":
    # Ensure the models list exists
    if not os.path.exists('models.txt'):
        with open('models.txt', 'w') as f: f.write("")

    with open('models.txt', 'r') as f:
        models = [m.strip() for m in f.readlines() if m.strip()]

    # Generate the results CSV
    with open('results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Model", "Brand", "Color", "Attributes", "Status"])
        writer.writeheader()
        for m in models:
            writer.writerow(mine_product(m))
