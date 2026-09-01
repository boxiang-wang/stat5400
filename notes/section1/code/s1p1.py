# STAT:5400 Section 1.1 — Introduction
# Code from the lecture notes; no output, no solutions.

## 17.1 Your first API call

from google import genai
client = genai.Client()               # reads GEMINI_API_KEY from the environment
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="In one sentence, what does a statistician do that a chatbot cannot?"
)
print(interaction.output_text)
