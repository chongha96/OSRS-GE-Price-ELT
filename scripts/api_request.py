import requests
import os

headers = {
        "User-Agent": "price tracking/storage ELT project - @viggora on discord"
    }

#Sends a request for current prices with Runescape Prices API
def fetch_price_data():
    api_url = "https://prices.runescape.wiki/api/v1/osrs/5m"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        print("API response successful")
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error occured: {e}")



#Cleans the list from the API request, populating missing values with None
def clean_price_data(price_data):
    if price_data is None:
        return []
    
    clean_items = []

    #Separating the list based on item_id. If it exists, append to the clean_items list
    for item_id, details in price_data.items():
        # Only process if the key is actually a numeric ID
        if item_id.isdigit():
            item_entry = details.copy()
            item_entry['id'] = int(item_id)
            clean_items.append(item_entry)


    #Desired keys for each dictionary object to have. If it does not contain it, add it with a value of None
    expected_keys = ['id', 'avgHighPrice', 'highPriceVolume', 'avgLowPrice', 'lowPriceVolume']

    #Nested loop. Iterates through each dictionary object in the clean_items list. Checks if all keys in expected_keys exist. If not, adds None
    for item in clean_items:
        for key in expected_keys:
            if key not in item:
                item[key] = None
                
    return clean_items



#Function to send a request for all item names & ids to create a dictionary
def fetch_item_data():
    api_url = "https://prices.runescape.wiki/api/v1/osrs/mapping"
    try:
        #Requesting data from weatherstack
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        print("API response successful")
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error occured: {e}")


#Cleans the list from the API request, populating missing values with None
def clean_item_data(items):
    if items is None:
        return []
    
    #Desired keys for each dictionary object to have. If it does not contain it, add it with a value of None
    expected_keys = ['id', 'name', 'examine', 'members', 'lowalch', 'highalch', 'value', 'limit', 'icon']

    #Nested loop. Iterates through each dictionary object in the clean_items list. Checks if all keys in expected_keys exist. If not, adds None
    for item in items:
        for key in expected_keys:
            if key not in item:
                item[key] = None
                
    return items