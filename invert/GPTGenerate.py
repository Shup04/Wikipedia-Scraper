
import json
import requests
import bs4

# Load the previously scraped inverts data
with open("inverts_data.json", "r", encoding="utf-8") as file:
    inverts = json.load(file)

# List to hold AI requests for entries that need additional info
ai_requests = []

def scrape_invert_details(url):
    """
    Scrapes a Wikipedia page for aquarium details using heuristic approaches.
    Attempts to extract an image URL from an infobox, and the first paragraph as a description.
    Also looks for rows in the infobox that mention size, tank, temperature, pH, or remarks.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        details = {}
        
        # Try to get the infobox (if any)
        infobox = soup.find("table", class_="infobox")
        if infobox:
            # Extract image URL from the infobox
            img_tag = infobox.find("img")
            if img_tag and img_tag.has_attr("src"):
                details["image_url"] = "https:" + img_tag["src"]
            # Loop through rows of the infobox to extract possible details
            for row in infobox.find_all("tr"):
                header = row.find("th")
                if header:
                    header_text = header.get_text(strip=True).lower()
                    td = row.find("td")
                    if not td:
                        continue
                    value = td.get_text(" ", strip=True)
                    if "size" in header_text and "tank" not in header_text:
                        details["size"] = value
                    elif "tank" in header_text:
                        details["tank_size"] = value
                    elif "temperature" in header_text:
                        details["temperature_range"] = value
                    elif "ph" in header_text:
                        details["ph_range"] = value
                    elif "remark" in header_text or "note" in header_text:
                        details["remarks"] = value

        # Get a brief description from the first paragraph in the main content
        content_div = soup.find("div", id="mw-content-text")
        if content_div:
            p_tag = content_div.find("p")
            if p_tag:
                details["description"] = p_tag.get_text(" ", strip=True)
        
        return details if details else None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def generate_ai_prompt(invert):
    """
    Builds a prompt to ask the AI (via OpenAI API) for additional aquarium details.
    """
    name = invert.get("name") or "Unknown Invertebrate"
    scientific_name = invert.get("scientific_name") or "Unknown Scientific Name"
    prompt = (
        f"Provide detailed aquarium information for the freshwater invertebrate '{name}' "
        f"(scientific name: {scientific_name}). Include the following details if available: "
        "an image URL, typical size, remarks, recommended tank size, temperature range, pH range, "
        "and a brief description. If certain details are unavailable from a source, please supply plausible values."
    )
    return prompt

# Process each invertebrate entry
for invert in inverts:
    link = invert.get("link", "")
    if link:
        print(f"Scraping details for: {invert.get('scientific_name', 'Unknown')} from {link}")
        details = scrape_invert_details(link)
        if details:
            invert.update(details)
        else:
            # If scraping returns no details, prepare an AI request for additional info
            prompt = generate_ai_prompt(invert)
            ai_requests.append({
                "custom_id": f"invert-{invert.get('id')}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o-2024-11-20",
                    "messages": [
                        {"role": "system", "content": "You are an expert in freshwater aquarium invertebrates."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 150,
                    "temperature": 0.2
                }
            })
    else:
        # No link provided, so prepare an AI request
        prompt = generate_ai_prompt(invert)
        ai_requests.append({
            "custom_id": f"invert-{invert.get('id')}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o-2024-11-20",
                "messages": [
                    {"role": "system", "content": "You are an expert in freshwater aquarium invertebrates."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 150,
                "temperature": 0.2
            }
        })

# Save the updated invertebrates data (including scraped details) to a new JSON file
with open("inverts_data_complete.json", "w", encoding="utf-8") as outfile:
    json.dump(inverts, outfile, indent=4)

# Write out the AI requests to a JSONL file for batch processing
with open("inverts_requests.jsonl", "w", encoding="utf-8") as jsonl_file:
    for req in ai_requests:
        jsonl_file.write(json.dumps(req) + "\n")

print("Scraping complete. Updated invertebrates data saved to 'inverts_data_complete.json'.")
print("AI batch request file created: 'inverts_requests.jsonl'.")
