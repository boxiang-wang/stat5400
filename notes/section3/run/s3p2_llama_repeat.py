# STAT 5400 - Section 3.2 - ask llama3.2:1b the same question 50 times, then a CI for P(correct)
# Runs on IDAS or in the Codespace. No API key needed. Takes about a minute.
# Uses the model's local address directly, so no extra Python package is needed.

# Start the Ollama server if it is not running yet (needed once per IDAS session)
import os, shutil, subprocess, time, urllib.request
def ollama_up():
    try:
        urllib.request.urlopen("http://localhost:11434/api/version", timeout=2)
        return True
    except OSError:
        return False
if not ollama_up():
    if os.path.isdir(os.path.expanduser("~/classdata/models")):   # on IDAS: use the class copy of Ollama and its models
        os.environ["PATH"] = os.path.expanduser("~/classdata/models/ollama/bin:") + os.environ["PATH"]
        os.environ["OLLAMA_MODELS"] = os.path.expanduser("~/classdata/models/library")
        os.environ["OLLAMA_NOPRUNE"] = "1"
    if shutil.which("ollama"):                                     # skip if Ollama is not installed
        subprocess.Popen("nohup ollama serve > ~/ollama.log 2>&1 &", shell=True)   # start it in the background
        for i in range(30):
            if ollama_up(): break
            time.sleep(1)

import json
from collections import Counter
from scipy.stats import binomtest

q = "Which is larger, 9.9 or 9.11? Answer with the number only."
answers = [""] * 50
for i in range(50):                                            # a new chat each time
    req = urllib.request.Request("http://localhost:11434/api/chat",
        data=json.dumps({"model": "llama3.2:1b", "stream": False,
                         "messages": [{"role": "user", "content": q}]}).encode(),
        headers={"Content-Type": "application/json"})
    answers[i] = json.load(urllib.request.urlopen(req))["message"]["content"].strip()
print(Counter(answers))

x = sum(a == "9.9" for a in answers)                           # number of correct answers
print(x)
res = binomtest(x, 50)
print(res.proportion_ci(method="wilson"))                      # Wilson interval
print(res.proportion_ci(method="exact"))                       # Clopper-Pearson (exact) interval
