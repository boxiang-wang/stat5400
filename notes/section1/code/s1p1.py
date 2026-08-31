# STAT:5400 Section 1.1 — Introduction
# Code from the lecture notes; no output, no solutions.

## 10 Demonstration of better implementation

import numpy as np, timeit
def tm(times=5, **fns):
    """tm(): the Python twin of timeit(); median wall-clock time in ms"""
    for name, f in fns.items():
        t = timeit.repeat(f, number=1, repeat=times)
        print(f"{name:>16s}: {1000*np.median(t):9.2f} ms")

x = np.random.rand(1_000_000)
tm(mean=lambda: x.mean(), sum_over_n=lambda: x.sum() / len(x))


## 17.1 Your first API call

from google import genai
client = genai.Client()               # reads GEMINI_API_KEY from the environment
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="In one sentence, what does a statistician do that a chatbot cannot?"
)
print(interaction.output_text)
