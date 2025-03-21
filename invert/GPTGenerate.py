import json
import re

def fix_missing_quote(json_str):
    """
    Heuristic fix: if the JSON string appears to have a missing closing quote in the description,
    insert one just before the , "refusal" substring.
    """
    fixed, count = re.subn(r'("description":\s*".*?)(, "refusal":)', r'\1"\2', json_str, flags=re.DOTALL)
    if count > 0:
        return fixed
    return json_str

def clean_newlines(json_str):
    """
    Remove newline characters that are not preceded by a backslash.
    This helps fix unterminated string errors due to unescaped newlines.
    """
    return re.sub(r'(?<!\\)\n', ' ', json_str)

def extract_json_from_content(content):
    """
    Extract and clean the JSON object from a response string that is wrapped in triple backticks.
    This function first extracts the text between the first '{' and the last '}', then applies
    cleaning steps and attempts to parse. If parsing fails after multiple fixes, it raises an error.
    """
    # Attempt to extract between the first '{' and last '}'
    start = content.find('{')
    end = content.rfind('}')
    if start == -1 or end == -1 or end < start:
        raise ValueError("No valid JSON object found in content.")
    json_str = content[start:end+1]
    json_str = json_str.replace("```", "").strip()
    
    # First attempt: parse as is
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # Remove unescaped newlines
        cleaned = clean_newlines(json_str)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e2:
            # Try to fix missing quote issues on the cleaned string
            fixed = fix_missing_quote(cleaned)
            try:
                return json.loads(fixed)
            except Exception as e3:
                raise ValueError(f"Failed to fix JSON after multiple attempts:\nOriginal: {json_str}\nAfter newline cleaning: {cleaned}\nAfter quote fix: {fixed}\nError: {e3}")

# Dictionary to hold successfully parsed responses mapped by invert id
responses = {}

# Open the batch responses file and process each line
with open("inverts_responses.jsonl", "r", encoding="utf-8") as infile:
    for line in infile:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception as e:
            print(f"Error loading JSONL line: {e}")
            continue

        custom_id = obj.get("custom_id", "")
        try:
            invert_id = int(custom_id.split("-")[1])
        except (IndexError, ValueError):
            print(f"Skipping invalid custom_id: {custom_id}")
            continue

        try:
            content = obj["response"]["body"]["choices"][0]["message"]["content"]
            details = extract_json_from_content(content)
            responses[invert_id] = details
        except Exception as e:
            print(f"Error processing response for {custom_id}: {e}")
            # Store the raw content for manual review if needed
            responses[invert_id] = {"error": "parsing_failed", "raw_response": content}

# Load the original inverts data
with open("inverts_data.json", "r", encoding="utf-8") as f:
    inverts = json.load(f)

# Inject the response details into the corresponding invert entries
for invert in inverts:
    invert_id = invert.get("id")
    if invert_id in responses:
        update_fields = responses[invert_id]
        if update_fields.get("error"):
            print(f"Invert-{invert_id} still has a parsing error; raw_response stored.")
        invert.update(update_fields)
    else:
        print(f"No valid response for invert-{invert_id}; leaving entry unchanged.")

# Save the updated data to a new file
with open("inverts_data_complete.json", "w", encoding="utf-8") as out_f:
    json.dump(inverts, out_f, indent=4)

print("Injection complete. Updated data saved to 'inverts_data_complete.json'.")
