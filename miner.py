import requests
from bs4 import BeautifulSoup
import csv
import re
import os

def mine_sku_data(model):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    # Targeted search query for the specific model
    search_url = f"https://www.google.com/search?q={model}+specifications+features"
    
    result = {
        "Model": model,
        "Color": "N/A",
        "Display_Type": "N/A",
        "Door_Split": "N/A",
        "Features": "N/A",
        "Progress": "Mined"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()

        # 1. Color Sniffer
        color_palette = ["Black", "White", "Silver", "Navy Blue", "Graphite", "Mint", "Gold"]
        for c in color_palette:
            if c.lower() in text:
                result["Color"] = c
                break

        # 2. Display Type Sniffer
        if "amoled" in text or "oled" in text: result["Display_Type"] = "AMOLED"
        elif "lcd" in text or "tft" in text: result["Display_Type"] = "LCD"

        # 3. Door / Split Type Sniffer
        if "split" in text: result["Door_Split"] = "Split AC"
        elif "double door" in text: result["Door_Split"] = "Double Door Fridge"

        # 4. Features Sniffer
        features_found = []
        if "inverter" in text: features_found.append("Inverter")
        if "fully automatic" in text: features_found.append("Fully Auto")
        result["Features"] = ", ".join(features_found) if features_found else "N/A"

    except Exception:
        result["Progress"] = "Error"

    return result

if __name__ == "__main__":
    if os.path.exists('models.txt'):
        with open('models.txt', 'r') as f:
            models = [line.strip() for line in f if line.strip()]
        
        with open('results.csv', 'w', newline='') as f:
            fieldnames = ["Model", "Color", "Display_Type", "Door_Split", "Features", "Progress"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for m in models:
                writer.writerow(mine_sku_data(m))
