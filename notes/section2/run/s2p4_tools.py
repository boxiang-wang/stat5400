# STAT 5400 - Section 2.4 - giving the model a function to call (Python, openai)
# Two tools, one question. The model must look up the column names before it can compute.
import json
import pandas as pd
from openai import OpenAI

client = OpenAI()
Cars = pd.read_csv("notes/section2/data/Cars.dat", sep="\t")

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
    raise ValueError(f"Unknown tool: {name}")

messages = [{"role": "user", "content": "What is the average weight of these cars?"}]

for step in range(5):
    resp = client.responses.create(model="gpt-5-nano", input=messages,
                                   instructions="Use the tools to compute. Never guess a number.",
                                   tools=TOOLS, parallel_tool_calls=False)
    messages += resp.output
    calls = [o for o in resp.output if o.type == "function_call"]
    if not calls:
        print(resp.output_text)
        break
    for c in calls:
        result = call_tool(c.name, json.loads(c.arguments or "{}"))
        print("->", c.name, c.arguments, "=>", result)
        messages.append({"type": "function_call_output",
                         "call_id": c.call_id, "output": json.dumps(result)})

# check the agent against the one line you could have written yourself
print(Cars["Weight"].mean())
