# STAT 5400 - Section 2.4 - roles, few-shot prompting, and structured output (Python, openai)
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

load_dotenv()
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
