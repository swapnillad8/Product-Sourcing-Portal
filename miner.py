import requests
from bs4 import BeautifulSoup
import re
import csv
import sys

def mine_product(model_no, region):
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = {"Model": model_no, "Brand": "Unknown", "Attributes": ""}
    
    # 1. SPECIAL CASE: APPLE (EveryMac)
    if re.match(r'A\d{4}', model_no):
        url = f"https://everymac.com/ultimate-mac-lookup/?search_keywords={model_no}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Logic to find SKU (Order Number)
        skus = soup.find_all(text=re.compile(r'[A-Z0-9]{5,9}/[A-Z]'))
        data["Brand"] = "Apple"
        data["Attributes"] = f"SKUs Found: {', '.join(set(skus[:5]))}"
        
    # 2. CASE: APPLIANCES (Search-based Mining)
    else:
        # Example: Search Google/Bing/DuckDuckGo for the OEM spec page
        search_query = f"{model_no} specifications inverter load type"
        # In a real scenario, you would scrape the top OEM result here
        data["Attributes"] = "Detected: Inverter, Fully Automatic, Front Load"
        
    return data

if __name__ == "__main__":
    # For testing: reads from a file called 'models.txt'
    with open('models.txt', 'r') as f:
        models = f.read().splitlines()
    
    with open('results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Model", "Brand", "Attributes"])
        writer.writeheader()
        for m in models:
            result = mine_product(m, "Global")
            writer.writerow(result)
