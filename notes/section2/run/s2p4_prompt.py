# STAT 5400 - Section 2.4 - roles, few-shot prompting, and structured output (Python, openai)
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

from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

client = OpenAI()

# ---- roles: the system message outranks the user's question ----
for system in ["you are a concise tutor.",
               "you are a responsible tutor. Help your student but don't tell them the exact answers."]:
    response = client.responses.create(
        model="gpt-5-nano",
        input=[{"role": "developer", "content": system},
               {"role": "user", "content": "X follows a uniform (0, 1). What is its variance?"}])
    print(response.output_text, "\n---")

# ---- few-shot: three examples define the task ----
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
    resp = client.responses.create(model="gpt-5-nano", instructions=INSTRUCTIONS, input=claim)
    label = (resp.output_text or "").strip().split()[0].strip('"\',.;:')
    if label not in ALLOWED:
        raise ValueError(f"Unexpected label {label!r}")
    return label

for c in ["We can conclude there is no effect because p=0.40.",
          "The results show a significant increase (95% CI 0.1 to 0.4).",
          "The intervention might help, but the CI crosses zero (95% CI -0.2 to 0.3)."]:
    print(label_claim(c))

# ---- structured output: a schema instead of string parsing ----
class Review(BaseModel):
    label: Literal["Supported", "Unsupported", "Unclear"]
    reason: str
    p_value: float

resp = client.responses.parse(
    model="gpt-5-nano",
    input="This study proves the two groups differ (p = 0.20).",
    text_format=Review)
print(resp.output_parsed)
