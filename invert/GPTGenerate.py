import json
import requests
import bs4

# Function to scrape details from a valid Wikipedia page
def scrape_info_from_link(url):
    info = {}
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Error fetching {url}: {response.status_code}")
            return info
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        # 1. Find the infobox table (with a <tbody>) and get the first <img>
        table = soup.find("table", class_="infobox")
        if table:
            tbody = table.find("tbody")
            if tbody:
                img_tag = tbody.find("img")
                if img_tag and img_tag.has_attr("src"):
                    info["image_url"] = "https:" + img_tag["src"]
        # 2. Extract description: get the first few nonempty <p> elements from the main content.
        content_div = soup.find("div", class_="mw-parser-output")
        description_text = ""
        if content_div:
            paragraphs = content_div.find_all("p")
            word_count = 0
            for p in paragraphs:
                # Skip empty paragraphs
                if p.get("class") and "mw-empty-elt" in p.get("class"):
                    continue
                text = p.get_text(" ", strip=True)
                if text:
                    description_text += text + "\n\n"
                    word_count += len(text.split())
                    if word_count >= 50:
                        break
        info["description"] = description_text.strip()
        # For now, other fields (size, remarks, tank_size, temperature_range, ph_range) remain empty
        info.setdefault("size", "")
        info.setdefault("remarks", "")
        info.setdefault("tank_size", "")
        info.setdefault("temperature_range", "")
        info.setdefault("ph_range", "")
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return info

def generate_prompt_for_valid(invert, scraped):
    """
    Build a prompt using the scraped info. The prompt includes the raw description (and image URL, if any)
    and instructs the AI to summarize the description into a concise summary and fill in any missing details.
    """
    name = invert.get("name", "Unknown invertebrate")
    scientific_name = invert.get("scientific_name", "Unknown scientific name")
    raw_desc = scraped.get("description", "")
    image_url = scraped.get("image_url", "")
    prompt = (
        f"The following data was scraped from the Wikipedia page for the invertebrate '{name}' "
        f"(scientific name: {scientific_name}).\n\n"
        f"Image URL: {image_url}\n\n"
        f"Raw description:\n{raw_desc}\n\n"
        "Please summarize this description into a concise summary that touches on key details such as appearance, "
        "habitat, and care requirements. Also, if possible, suggest plausible values for size, remarks, recommended tank size, "
        "temperature range, and pH range. Return your answer as valid JSON with the keys: image_url, size, remarks, tank_size, "
        "temperature_range, ph_range, description."
    )
    return prompt

def generate_prompt_for_redlink(invert):
    """
    Build a prompt for cases where the Wikipedia link is a redlink or missing.
    """
    name = invert.get("name", "Unknown invertebrate")
    scientific_name = invert.get("scientific_name", "Unknown scientific name")
    prompt = (
        f"Provide complete freshwater aquarium information for the invertebrate '{name}' "
        f"(scientific name: {scientific_name}). Include an image URL, typical size, any remarks, "
        "recommended tank size, temperature range, pH range, and a brief concise description that touches on key details. "
        "If no reliable source exists, invent plausible details. Return your answer in valid JSON format with the keys: "
        "image_url, size, remarks, tank_size, temperature_range, ph_range, description."
    )
    return prompt

# Load the previously scraped inverts JSON data (with basic info including the link)
with open("inverts_data.json", "r", encoding="utf-8") as f:
    inverts = json.load(f)

# Prepare a list to hold batch requests (one JSON object per line)
batch_requests = []

for invert in inverts:
    link = invert.get("link", "")
    # Determine if link is valid (i.e. not a redlink)
    if link and "redlink=1" not in link:
        full_url = "https://en.wikipedia.org" + link if link.startswith("/") else link
        print(f"Scraping: {full_url}")
        scraped = scrape_info_from_link(full_url)
        prompt = generate_prompt_for_valid(invert, scraped)
    else:
        print(f"Redlink or missing link for: {invert.get('scientific_name', 'Unknown')}. Generating full info.")
        prompt = generate_prompt_for_redlink(invert)
    
    request_data = {
        "custom_id": f"invert-{invert.get('id', 'unknown')}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-2024-11-20",
            "messages": [
                {"role": "system", "content": "You are an expert in freshwater aquarium invertebrates."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.2
        }
    }
    batch_requests.append(request_data)

# Write out all batch requests to a JSONL file (one JSON object per line)
output_file = "inverts_requests.jsonl"
with open(output_file, "w", encoding="utf-8") as jsonl_file:
    for req in batch_requests:
        jsonl_file.write(json.dumps(req) + "\n")

print(f"Batch request file created: {output_file}")
