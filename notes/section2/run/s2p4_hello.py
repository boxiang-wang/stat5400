# STAT 5400 - Section 2.4 - your first LLM API call (Python, openai)
# The key is a Codespaces secret. Never write it in this file.
# Check the OpenAI key, and on IDAS use the class copy of the openai package
import os, sys, urllib.request
if os.path.isdir(os.path.expanduser("~/classdata/models/python")):          # on IDAS
    sys.path.insert(0, os.path.expanduser("~/classdata/models/python"))     # class packages first
    sys.modules.pop("typing_extensions", None)                              # forget the old system copy
renviron = os.path.expanduser("~/.Renviron")                                # read the key from the file R uses
if os.path.exists(renviron):
    for line in open(renviron):
        name, _, value = line.strip().partition("=")
        if name and not name.startswith("#") and value:
            os.environ.setdefault(name, value.strip("\"'"))
help_url = "https://boxiang-wang.github.io/stat5400/notes/section2/s2p4.html#setting-up-idas"
if not os.environ.get("OPENAI_API_KEY"):
    print("No OpenAI key found. How to set it up:", help_url)
else:
    try:
        urllib.request.urlopen(urllib.request.Request("https://api.openai.com/v1/models",
            headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}), timeout=10)
    except OSError:
        print("Your OpenAI key did not work. Check it, or see:", help_url)

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
