# STAT 5400 - Section 2.4 - your first LLM API call (Python, openai)
# The key is a Codespaces secret. Never write it in this file.
import os
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input=[{"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}],
)
print(response.output_text)

# Every request is stateless: a second, separate call remembers nothing.
r1 = client.responses.create(
    model="gpt-5-nano",
    input=[{"role": "user", "content": "Write a paragraph about the Department of Statistics "
                                       "and Actuarial Science at the University of Iowa."}])
print(r1.output_text)

r2 = client.responses.create(
    model="gpt-5-nano",
    input=[{"role": "user", "content": "What's the name of the university that I just mentioned?"}])
print(r2.output_text)        # it does not know

# Three ways to give it a memory. This is the third: let the provider keep the thread.
r3 = client.responses.create(
    model="gpt-5-nano",
    input=[{"role": "user", "content": "Write two sentences about the University of Iowa."}],
    store=True)
print(r3.output_text)

r4 = client.responses.create(
    model="gpt-5-nano",
    previous_response_id=r3.id,
    input=[{"role": "user", "content": "What is the name of the university I just mentioned?"}],
    store=True)
print(r4.output_text)
