import bs4
import json
#from openai import OpenAI
from GPTSummarize import generateGPTResponse

# Load the HTML content from filke
with open("./wikipage.html", "r", encoding="utf-8") as file:
    soup = bs4.BeautifulSoup(file, 'html.parser')

# list of fish groups
groups_with_subgroups = {
    "Catfish": ["Armored Catfish", "Armoured Suckermouth Catfish", "Long-whiskered Catfish", "Squeakers & Upside-down Catfish", "Other Catfish"],
    "Characins & Other Characiformes": ["Tetras", "Hatchetfish", "Pencilfish", "Serrasalminae", "Other Characins"],
    "Cichlids": ["Lake Malawi Cichlids", "Lake Tanganyika Cichlids", "Lake Victorio Cichlids", "Miscellaneous African Cichlids", "Dwarf Cichlids", "Central American Cichlids", "South American", "Other Cichlids"],
    "Cyprinids": ["Barbs", "Other Cyprinids", "Rasboras", "Danios & Other Danionins", "Cold-water Cyprinids"],
    "Loaches & Related Cypriniformes": ["Loaches"],
    "Livebearers & Killifish": ["Guppies & Mollies", "", "Platies & Swordtails", "Other Livebearers", "Killifish"],
    "Labyrinth Fish": ["Gouramis", "Other Labyrinth Fish"],
    "Rainbowfish": ["Rainbowfish"],
    "Gobies & Sleepers": ["Gobies & Sleepers"],
    "Others": ["Others"]
}

unique_id = 1
fish_data = []

for group, subgroups in groups_with_subgroups.items():
    for subgroup in subgroups:

        # scrape all tables from page
        table = soup.find('table', class_=["sortable", "wikitable"])
        if table is None:
            print(f"No table found for {subgroup} in {group}")
            continue
        
        # Process each row in the found table, skipping the header row
        rows = table.find_all('tr')[1:]  # Skip header
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 8:  # Ensuring there are enough columns
                continue

            # Extracting cell text, image URLs, and hyperlinks
            common_name = cols[0].text.strip()
            scientific_name = cols[1].text.strip()
            img_tag = cols[2].find('img')
            image_url = f"https:{img_tag['src']}" if img_tag else ""
            size = cols[3].text.strip()
            remarks = cols[4].text.strip()
            tank_size = cols[5].text.strip()
            temp_range = cols[6].text.strip()
            ph_range = cols[7].text.strip()
            
            fish_data.append({
                "id": unique_id,
                "common_name": common_name,
                "scientific_name": scientific_name,
                "image_url": image_url,
                "size": size,
                "remarks": remarks,
                "tank_size": tank_size,
                "temperature_range": temp_range,
                "ph_range": ph_range,
                "group": group,
                "subgroup": subgroup
            })
            unique_id += 1
        
        # Remove the processed table to avoid reprocessing it in the next iteration
        table.decompose()

# Saving the scraped data to a JSON file
with open("fish_data_with_groups.json", "w", encoding="utf-8") as f:
    json.dump(fish_data, f, indent=4)

print("Data scraping completed and saved to fish_data_with_groups.json.")
