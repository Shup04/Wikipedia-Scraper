import openai
import time

from openai import OpenAI
client = OpenAI()

# Replace with your actual batch job ID
batch_id = "batch_67ddbe2aa924819087f5c702499d39ee"

# Poll the batch job until it is complete.
while True:
    job = openai.batches.retrieve(batch_id)
    print(f"Batch job status: {job.status}")
    if job.status == "completed":
        break
    time.sleep(10)  # Wait 10 seconds before checking again

# Once complete, the output_file_id will be available
output_file_id = job.output_file_id
print(f"Output file ID: {output_file_id}")

# Download the output file
response = client.files.content(output_file_id)
# Get the raw bytes from the response object
output_bytes = response.content

# Save the response to a local file
with open("inverts_responses.jsonl", "wb") as f:
    f.write(output_bytes)

print("Downloaded batch responses to 'inverts_responses.jsonl'.")
