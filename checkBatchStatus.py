from openai import OpenAI

client = OpenAI()

# Step 3: Check the status of your batch using its ID.
# Replace "batch_abc123" with your actual batch ID.
batch = client.batches.retrieve("batch_67c4cbe3b79881908feda6cb417cea47")
print("Batch status and metadata:")
print(batch)

# Step 4: Once the batch is complete, retrieve the output.
# The Batch object contains an 'output_file_id' field.
# Replace "file-xyz123" with the actual output file ID from your batch object.
file_response = client.files.content("file-3AsCRt649kjYPfR14pcYyt")
#print("Batch output:")
#print(file_response.text)

# Optionally, write the output to a local file.
with open("batch_output.jsonl", "w", encoding="utf-8") as f:
    f.write(file_response.text)

print("Batch output saved to batch_output.jsonl")
