
from openai import OpenAI

# Instantiate the client (ensure your API key is set in your environment)
client = OpenAI()

# Step 1: Upload your JSONL file for batch processing.
batch_input_file = client.files.create(
    file=open("fish_requests.jsonl", "rb"),
    purpose="batch"
)
print("Uploaded file info:", batch_input_file)

# Step 2: Create a batch job using the uploaded file's ID.
# For this example, we'll use a completion window of 24 hours and include custom metadata.
batch = client.batches.create(
    input_file_id=batch_input_file.id,  # Use the file ID from the uploaded file
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
        "description": "Fish popularity nightly eval job"
    }
)
print("Batch job created:", batch)
