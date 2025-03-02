import json
import re

DEFAULT_RANK = 13

# Load original fish data
with open("fish_data.json", "r", encoding="utf-8") as f:
    fish_data = json.load(f)

# Build an ordered list of popularity scores from the batch output file.
# We assume that the batch output file's lines (in order) correspond to fish with non-empty names.
valid_popularity_scores = []
with open("batch_output.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        record = json.loads(line)
        try:
            # Extract the response text from the nested structure.
            content = record["response"]["body"]["choices"][0]["message"]["content"]
            # Use regex to search for the first number in the content.
            match = re.search(r'\d+', content)
            if match:
                score = int(match.group(0))
            else:
                # If no number is found, assign the default rank.
                score = DEFAULT_RANK
        except Exception as e:
            print(f"Error parsing score for record with custom_id {record.get('custom_id')}: {e}")
            score = DEFAULT_RANK
        valid_popularity_scores.append(score)

# Now inject the popularity scores into the original fish data.
# We assume the ordering of valid responses corresponds to fish with non-empty names.
valid_index = 0
for fish in fish_data:
    if fish is None:
        continue
    name = fish.get("name", "").strip()
    if name:  # Fish that were processed in the batch
        if valid_index < len(valid_popularity_scores):
            fish["popularity_score"] = valid_popularity_scores[valid_index]
            valid_index += 1
        else:
            fish["popularity_score"] = DEFAULT_RANK
    else:
        # For fish with no name, assign the default middle ranking.
        fish["popularity_score"] = DEFAULT_RANK

# Save the updated fish data to a new JSON file.
with open("updated_fish_data.json", "w", encoding="utf-8") as f:
    json.dump(fish_data, f, indent=4)

print("Updated fish_data with popularity scores saved to 'updated_fish_data.json'.")
