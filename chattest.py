from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are to summarise fish information into a digestible format for a mobile app in one consice paragraph."},
        {"role": "user", "content": "Corydoras geoffroy is a tropical freshwater fish belonging to the Corydoradinae sub-family of the family Callichthyidae. It originates in coastal rivers in South America, and is found in Suriname and French Guiana.  It is the type species of the genus Corydoras. The fish will grow in length up to 2.8 inches (7.0 centimeters). It lives in a tropical climate in water with a 6.0 – 8.0 pH, a water hardness of 2 – 25 dGH, and a temperature range of 72 – 79 °F (22 – 26 °C). It feeds on worms, benthic crustaceans, insects, and plant matter. It lays eggs in dense vegetation and adults do not guard the eggs. "},
    ],
    temperature=0,
)

print(response)