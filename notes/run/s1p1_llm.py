# STAT 5400 - Section 1.1 - Your first LLM API call (Python, google-genai)
# Needs GEMINI_API_KEY in the environment (Codespaces secret). Never put the key in this file.
from google import genai

client = genai.Client()   # reads GEMINI_API_KEY

q = "In one sentence, what does a statistician do that a chatbot cannot?"
for _ in range(2):        # twice: is the answer identical? (An LLM is a sampler.)
    interaction = client.interactions.create(model="gemini-3.7-flash", input=q)
    print(interaction.output_text)
