import bs4
import json

# Load the HTML content from the saved Inverts.html file
with open("Inverts.html", "r", encoding="utf-8") as file:
    soup = bs4.BeautifulSoup(file, "html.parser")

unique_id = 1
inverts_data = []

# Find all <li> elements; adjust the container if needed
li_items = soup.find_all("li")

for li in li_items:
    # Check for an <i> tag containing an <a> element
    i_tag = li.find("i")
    if not i_tag:
        continue
    a_tag = i_tag.find("a", href=True)
    if not a_tag:
        continue

    # Use the full text of the li and split by comma.
    # Expected format: "Arachnochium kulsiense, Sand shrimp"
    full_text = li.get_text(separator=" ", strip=True)
    parts = full_text.split(",", 1)
    scientific_name = parts[0].strip()
    common_name = parts[1].strip() if len(parts) > 1 else ""

    # Construct the full URL for the link
    link = a_tag.get("href")
    description_url = f"{link}" if link else ""

    # Append the scraped data using the desired JSON structure
    inverts_data.append({
        "id": unique_id,
        "name": common_name,
        "scientific_name": scientific_name,
        "image_url": "",
        "size": "",
        "remarks": "",
        "tank_size": "",
        "temperature_range": "",
        "ph_range": "",
        "group": "Invertebrates",
        "subgroup": "",
        "link": description_url,
        "description": ""
    })
    unique_id += 1

# Save the scraped data to a JSON file
with open("inverts_data.json", "w", encoding="utf-8") as f:
    json.dump(inverts_data, f, indent=4)

print("Data scraping completed and saved to inverts_data.json.")
