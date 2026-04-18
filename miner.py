import requests
from bs4 import BeautifulSoup
import csv
import os

def mine_sku_data(model):
    # Updated headers to prevent blocking and speed up response
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    # Targeted search for faster result isolation
    search_url = f"https://www.google.com/search?q=Samsung+India+{model}+specs+color"
    
    result = {
        "Model": model,
        "Color": "N/A",
        "Display_Type": "N/A",
        "Door_Split": "N/A",
        "Features": "N/A",
        "Progress": "Mined"
    }

    try:
        # Reduced timeout to 10s to prevent long hangs
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()

        # Fast keyword matching
        if "black" in text: result["Color"] = "Phantom Black"
        if "blue" in text: result["Color"] = "Spotlight Blue"
        if "amoled" in text: result["Display_Type"] = "AMOLED"
        if "inverter" in text: result["Features"] = "Inverter"
        
    except Exception:
        result["Progress"] = "Error"

    return result

if __name__ == "__main__":
    # Ensure this reads the latest models input by you in the UI
    if os.path.exists('models.txt'):
        with open('models.txt', 'r') as f:
            models = [line.strip() for line in f if line.strip()]
        
        with open('results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Model", "Color", "Display_Type", "Door_Split", "Features", "Progress"])
            writer.writeheader()
            for m in models:
                writer.writerow(mine_sku_data(m))
