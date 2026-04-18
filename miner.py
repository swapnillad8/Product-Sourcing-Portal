import requests
from bs4 import BeautifulSoup
import csv
import re
import os

def mine_product(model):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    # Searching specifically for technical specifications
    url = f"https://www.google.com/search?q={model}+specifications+features"
    
    result = {
        "Model": model,
        "Display_Type": "N/A",
        "Door_Split": "N/A",
        "Features": "N/A",
        "Status": f"Not Found: {model}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().lower()

        # 1. DISPLAY TYPE (AMOLED, LCD, LED, OLED)
        display_types = ["amoled", "super amoled", "lcd", "led", "oled", "tft"]
        for d in display_types:
            if d in page_text:
                result["Display_Type"] = d.upper()
                break

        # 2. DOOR / SPLIT TYPE (Top Load, Front Load, Split AC, Double Door)
        types = ["top load", "front load", "split", "window", "double door", "single door"]
        for t in types:
            if t in page_text:
                result["Door_Split"] = t.title()
                break

        # 3. FEATURES (Inverter, Automatic, Fully Automatic)
        features = []
        if "inverter" in page_text: features.append("Inverter")
        if "fully automatic" in page_text: features.append("Fully Auto")
        elif "semi automatic" in page_text: features.append("Semi Auto")
        result["Features"] = ", ".join(features) if features else "N/A"

        # STATUS LOGIC
        if result["Display_Type"] != "N/A" or result["Features"] != "N/A":
            result["Status"] = f"Found: {model}"
        else:
            result["Status"] = f"Partial Found: {model}"

    except Exception:
        result["Status"] = f"Error: {model}"

    return result

if __name__ == "__main__":
    if os.path.exists('models.txt'):
        with open('models.txt', 'r') as f:
            models = [line.strip() for line in f if line.strip()]
        
        with open('results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Model", "Display_Type", "Door_Split", "Features", "Status"])
            writer.writeheader()
            for m in models:
                writer.writerow(mine_product(m))
