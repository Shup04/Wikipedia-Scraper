
import json

def extract_json_from_content(content):
    """
    Remove markdown code block formatting (triple backticks) and parse the JSON.
    """
    # Remove starting "```json" if present
    if content.startswith("```json"):
        content = content[len("```json"):].strip()
    # Remove trailing triple backticks if present
    if content.endswith("```"):
        content = content[:-len("```")].strip()
    return json.loads(content)

# Load batch responses from the JSONL file
responses = {}
with open("inverts_responses.jsonl", "r", encoding="utf-8") as infile:
    for line in infile:
        if not line.strip():
            continue
        obj = json.loads(line)
        # custom_id is like "invert-1", extract the numeric part and convert to int
        custom_id = obj.get("custom_id", "")
        try:
            invert_id = int(custom_id.split("-")[1])
        except (IndexError, ValueError):
            continue
        # Extract the assistant's content from the response structure
        try:
            content = obj["response"]["body"]["choices"][0]["message"]["content"]
            # Parse out the JSON from the code block
            details = extract_json_from_content(content)
            responses[invert_id] = details
        except Exception as e:
            print(f"Error processing response for {custom_id}: {e}")

# Load the original inverts data
with open("inverts_data.json", "r", encoding="utf-8") as f:
    inverts = json.load(f)

# Inject the response details into the corresponding invert entries
for invert in inverts:
    invert_id = invert.get("id")
    if invert_id in responses:
        # Update the fields: image_url, size, remarks, tank_size, temperature_range, ph_range, description
        update_fields = responses[invert_id]
        invert.update(update_fields)

# Save the updated data to a new file
with open("inverts_data_complete.json", "w", encoding="utf-8") as out_f:
    json.dump(inverts, out_f, indent=4)

print("Injection complete. Updated data saved to 'inverts_data_complete.json'.")
