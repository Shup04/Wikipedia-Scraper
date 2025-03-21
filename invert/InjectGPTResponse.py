import json
import re

def fix_missing_quote(json_str):
    """
    A heuristic fix: if the JSON string appears to have a missing closing quote in the description,
    insert one just before the , "refusal" substring.
    """
    # Look for a pattern like: ("description":\s*".*?)(, "refusal":)
    fixed, count = re.subn(r'("description":\s*".*?)(, "refusal":)', r'\1"\2', json_str, flags=re.DOTALL)
    if count > 0:
        return fixed
    return json_str

def extract_json_from_content(content):
    """
    Extract the JSON object from a response string that is wrapped in triple backticks.
    Attempts to use regex to capture the JSON text. If json.loads fails, it will try to fix common issues.
    """
    # Try to capture content between ```json and ```
    match = re.search(r"```json\s*(\{.*\})\s*```", content, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Fallback: find the first { and last }
        start = content.find('{')
        end = content.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_str = content[start:end+1]
        else:
            raise ValueError("No JSON object found in the content.")
    
    json_str = json_str.replace("```", "").strip()
    
    # First attempt to load
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # If error indicates an unterminated string, attempt to fix it
        if "Unterminated string" in str(e) or "Extra data" in str(e):
            fixed_str = fix_missing_quote(json_str)
            try:
                return json.loads(fixed_str)
            except Exception as e2:
                raise ValueError(f"Failed to fix JSON: {e2}\nOriginal: {json_str}\nFixed: {fixed_str}")
        else:
            raise

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
  
