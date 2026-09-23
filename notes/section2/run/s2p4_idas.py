# STAT 5400 - Section 2.4 - LLM APIs and Prompting
# All the Python code from the page, set up for IDAS.
# Page: https://boxiang-wang.github.io/stat5400/notes/section2/s2p4.html
#
# Before you start
# 1. Start the class models once per session. In a Terminal, type:
#      source ~/classFiles/notes/section2/run/s2p4_idas_models.sh
# 2. For the OpenAI parts, put your API key in the file ~/.Renviron (the same file R uses):
#      OPENAI_API_KEY=your-openai-key
#    Never type a key into this file.
# 3. Run it all with:
#      python ~/classFiles/notes/section2/run/s2p4_idas.py
#    It takes a few minutes. The OpenAI calls use gpt-5-nano and cost a fraction of a cent.

import os, sys
sys.path.insert(0, os.path.expanduser("~/classdata/models/python"))   # class packages first
from openai import OpenAI

# Read your keys from ~/.Renviron: one NAME=value per line
renviron = os.path.expanduser("~/.Renviron")
if os.path.exists(renviron):
    for line in open(renviron):
        name, _, value = line.strip().partition("=")
        if name and not name.startswith("#"):
            os.environ.setdefault(name, value.strip('"\''))

client = OpenAI()                                                        # OpenAI, reads OPENAI_API_KEY
local = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")   # the class models on IDAS

## 3.1 Hello world

response = client.responses.create(
    model="gpt-5-nano",
    input=[{"role": "user", "content":
            "Write a one-sentence bedtime story about a unicorn."}],
)
print(response.output_text)


## 3.2 Open-weight models

resp = local.chat.completions.create(
    model="llama3.2:1b",                         # 1 billion parameters
    messages=[{"role": "user",
               "content": "Give me 3 distributions in the exponential family."}])
print(resp.choices[0].message.content)

resp = local.chat.completions.create(
    model="qwen3.5:4b", reasoning_effort="none", # IDAS only; skip the thinking step
    messages=[{"role": "user",
               "content": "Give me 3 distributions in the exponential family."}])
print(resp.choices[0].message.content)


## 4.2 Roles

for system in ["you are a concise tutor.",
               "you are a responsible tutor. Help your student "
               "but don't tell them the exact answers."]:
    response = client.responses.create(
        model="gpt-5-nano",
        input=[{"role": "developer", "content": system},
               {"role": "user", "content":
                "X follows a uniform (0, 1). What is its variance?"}])
    print(response.output_text, "\n---")


## 4.3 The model does not remember earlier calls

r1 = client.responses.create(
    model="gpt-5-nano",
    input=[{"role": "user", "content":
            "Write a paragraph about the Department of Statistics and Actuarial "
            "Science at the University of Iowa."}])
print(r1.output_text)

r2 = client.responses.create(
    model="gpt-5-nano",
    input=[{"role": "user", "content":
            "What's the name of the university that I just mentioned?"}])
print(r2.output_text)     # it does not know


## 4.4 Conversation state

response = client.responses.create(
    model="gpt-5-nano",
    input=[{"role": "user",      "content": "knock knock."},
           {"role": "assistant", "content": "Who's there?"},
           {"role": "user",      "content": "Felix"}])
print(response.output_text)

history = [{"role": "user", "content": "Tell me a joke about statistics."}]
response = client.responses.create(model="gpt-5-nano", input=history)
print(response.output_text)

history.append({"role": "assistant", "content": response.output_text})   # add to the end
history.append({"role": "user", "content": "Tell me another."})
response = client.responses.create(model="gpt-5-nano", input=history)
print(response.output_text)

response = client.responses.create(
    model="gpt-5-nano",
    input="Tell me a joke about statistics.")
print(response.output_text)

second = client.responses.create(
    model="gpt-5-nano",
    previous_response_id=response.id,    # the ID of the last reply
    input="Explain why this is funny.")
print(second.output_text)


## 4.5 Few-shot learning

INSTRUCTIONS = """# Identity

You are a helpful assistant that labels short statistical claims as
Supported, Unsupported, or Unclear based on the evidence provided.

# Instructions

* Only output a single word, with no additional formatting or commentary.
* Your response must be one of "Supported", "Unsupported", or "Unclear".

# Examples

<stat_claim id="example-1">
The new drug lowered systolic blood pressure
(mean difference -5.2 mmHg, 95% CI -8.1 to -2.3, p=0.001).
</stat_claim>
<assistant_response id="example-1">Supported</assistant_response>

<stat_claim id="example-2">
This study proves the two groups are different
(mean difference 1.1, 95% CI -0.6 to 2.8, p=0.20).
</stat_claim>
<assistant_response id="example-2">Unsupported</assistant_response>

<stat_claim id="example-3">
The treatment improved outcomes, but only a trend was observed (p=0.07).
</stat_claim>
<assistant_response id="example-3">Unclear</assistant_response>
"""

ALLOWED = {"Supported", "Unsupported", "Unclear"}

def label_claim(claim):
    resp = client.responses.create(model="gpt-5-nano",
                                   instructions=INSTRUCTIONS, input=claim)
    label = (resp.output_text or "").strip().split()[0].strip('"\',.;:')
    if label not in ALLOWED:
        raise ValueError(f"Unexpected label {label!r}")
    return label

for c in ["We can conclude there is no effect because p=0.40.",
          "The results show a significant increase (95% CI 0.1 to 0.4).",
          "The intervention might help, but the CI crosses zero (95% CI -0.2 to 0.3)."]:
    print(label_claim(c))


## 5.1 Ask for a type, not a string

from pydantic import BaseModel
from typing import Literal

class Review(BaseModel):
    label: Literal["Supported", "Unsupported", "Unclear"]
    reason: str
    p_value: float

resp = client.responses.parse(
    model="gpt-5-nano",
    input="This study proves the two groups differ (p = 0.20).",
    text_format=Review)
print(resp.output_parsed.label, resp.output_parsed.p_value)


## 6.2 Watch a small model fail, then fix it

import json

def larger(a, b):
    a, b = float(a), float(b)          # small models sometimes send "9.9" as text
    return max(a, b)

TOOLS = [{"type": "function", "function": {
    "name": "larger",
    "description": "Return the larger of two numbers.",
    "parameters": {"type": "object",
                   "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                   "required": ["a", "b"]}}}]

msgs = [{"role": "system", "content": "Use the tool to compare numbers."},
        {"role": "user", "content": "Which is larger, 9.9 or 9.11?"}]

# steps 1 and 2: send the question with the tool, and read the model's request
reply = local.chat.completions.create(model="llama3.2:1b", messages=msgs, tools=TOOLS)
msgs.append(reply.choices[0].message)

# step 3: run the function and send its result back
for call in reply.choices[0].message.tool_calls or []:
    args = json.loads(call.function.arguments)
    print("->", call.function.name, args)
    msgs.append({"role": "tool", "tool_call_id": call.id,
                 "content": str(larger(**args))})

# step 4: the model answers, using the result
final = local.chat.completions.create(model="llama3.2:1b", messages=msgs, tools=TOOLS)
print(final.choices[0].message.content)


## 6.3 A two-tool example

import json, pandas as pd
Cars = pd.read_csv(os.path.expanduser("~/classFiles/notes/section2/data/Cars.dat"), sep="\t")

TOOLS = [
  {"type": "function", "name": "column_names",
   "description": "List the column names of the cars data set.",
   "parameters": {"type": "object", "properties": {},
                  "required": [], "additionalProperties": False},
   "strict": True},
  {"type": "function", "name": "column_mean",
   "description": "Return the mean of one numeric column of the cars data set.",
   "parameters": {"type": "object",
                  "properties": {"column": {"type": "string"}},
                  "required": ["column"], "additionalProperties": False},
   "strict": True},
]

def call_tool(name, args):
    if name == "column_names":
        return ", ".join(Cars.columns)
    if name == "column_mean":
        column = args["column"]
        if column not in Cars.columns:
            return f"There is no column named {column}."    # the model reads this and retries
        return float(Cars[column].mean())

messages = [{"role": "user", "content": "What is the average weight of these cars?"}]
for step in range(5):
    resp = client.responses.create(model="gpt-5-nano", input=messages,
                                   instructions="Use the tools to compute. Never guess a number.",
                                   tools=TOOLS, parallel_tool_calls=False)
    messages += resp.output
    calls = [o for o in resp.output if o.type == "function_call"]
    if not calls:
        print(resp.output_text); break
    for c in calls:
        result = call_tool(c.name, json.loads(c.arguments or "{}"))
        print("->", c.name, c.arguments, "=>", result)
        messages.append({"type": "function_call_output",
                         "call_id": c.call_id, "output": json.dumps(result)})
