from concurrent.futures import ThreadPoolExecutor
import requests
import json
from bs4 import BeautifulSoup
from GPTSummarize import generateGPTResponse

# Load the initial data
with open('fish_data_links.json', 'r') as file:
    fish_data_list = json.load(file)

# Function to fetch and process the description
def fetch_description(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        specific_div = soup.find('div', class_='mw-content-ltr mw-parser-output')
        all_paragraph_text = " ".join(paragraph.text.strip() for paragraph in specific_div.find_all('p'))
        if specific_div:
            return generateGPTResponse(all_paragraph_text)
    return "Description not available."

# Enrich data with descriptions (replacing URLs)
def enrich_data(fish_data):
    if 'link' in fish_data:
        description = fetch_description(fish_data['link'])
        print('Saving fish id: ', fish_data['id'])
        fish_data['description'] = description
        del fish_data['link']  # Optionally remove the URL
    return fish_data

# Using ThreadPoolExecutor to parallelize fetching descriptions
with ThreadPoolExecutor(max_workers=20) as executor:
    # Enrich each fish data entry with its description
    fish_data_enriched = list(executor.map(enrich_data, fish_data_list))

# Save the enriched data to a new JSON file
with open('fish_data_descriptions.json', 'w') as file:
    json.dump(fish_data_enriched, file, indent=4)
