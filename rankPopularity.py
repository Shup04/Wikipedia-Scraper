import json

# Load fish data from JSON
input_file = "./inverts_data_complete.json"
output_file = "./invert_requests.jsonl"

with open(input_file, "r", encoding="utf-8") as file:
    fish_data = json.load(file)

# Function to generate a prompt safely
def generate_prompt(fish):
    # Use a fallback if "name" or "scientific_name" is missing or empty
    name = fish.get("name") or "Unknown Fish"
    scientific_name = fish.get("scientific_name") or "Unknown Scientific Name"
    
    return (
        f"Rate the popularity of the freshwater aquarium fish '{name}' "
        f"(scientific name: {scientific_name}) on a scale of 1 to 25, "
        "with 25 being the most popular and 1 being the least. Consider factors such as "
        "how commonly it is kept in aquariums, and its availability in pet stores."
        "Respond only with a single integer value."
    )

# OpenAI model to use
model = "gpt-4-turbo"

# Create JSONL file for batch processing
with open(output_file, "w", encoding="utf-8") as jsonl_file:
    for i, fish in enumerate(fish_data):
        # In case a fish entry is None, skip it
        if fish is None:
            continue

        request_data = {
            "custom_id": f"fish-{i+1}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are an expert in freshwater aquariums."},
                    {"role": "user", "content": generate_prompt(fish)}
                ],
                "max_tokens": 5,
                "temperature": 0.2  # Low randomness for consistent responses
            }
        }
        jsonl_file.write(json.dumps(request_data) + "\n")

print(f"JSONL batch request file created: {output_file}")
