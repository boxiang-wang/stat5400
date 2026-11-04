# STAT:5400 Section 5.1 — AI Agents
# Code from the lecture notes; no output, no solutions.

## 3.1 A stand-in agent, for simulation

import numpy as np

aircondit = np.array([3, 5, 7, 18, 43, 85, 91, 98, 100, 130, 230, 487])   # hours between failures, HW 9
DATA = {"aircondit": aircondit}

def describe(name):
    """Describe a data vector: its length, mean, and median.
    Call this before bootstrapping."""
    x = DATA[name]
    return f"{len(x)} values; mean {x.mean():.1f}; median {np.median(x):.1f}"

def boot_se(name, stat, B=2000, seed=5400):
    """Bootstrap standard error of a statistic ("mean" or "median") of a data vector."""
    x = DATA[name]
    f = {"mean": np.mean, "median": np.median}[stat]
    rng = np.random.default_rng(seed)
    est = [f(rng.choice(x, size=len(x), replace=True)) for _ in range(B)]
    return {"estimate": round(float(f(x)), 4), "se": round(float(np.std(est, ddof=1)), 4)}

tools = {"describe": describe, "boot_se": boot_se}

print(describe("aircondit"))
print(boot_se("aircondit", stat="mean", B=2000))

def run_agent(model, tools, task, max_steps=6):
    history, receipt = [task], []
    for step in range(1, max_steps + 1):
        action = model(history, list(tools))        # 1. ask the model what to do
        if "final" in action:                       # 2. it answered: stop
            receipt.append((step, "(answer)", "", action["final"]))
            return {"answer": action["final"], "receipt": receipt, "steps": step}
        try:                                        # 3. run the tool it asked for
            result = tools[action["tool"]](**action["args"])
        except Exception as e:
            result = f"ERROR: {e}"
        receipt.append((step, action["tool"], str(action["args"]), str(result)))
        history.append(f"{action['tool']}: {result}")  # 4. show the result
    return {"answer": None, "receipt": receipt, "steps": max_steps}   # 5. out of steps

def show(receipt):
    for row in receipt:
        print(*row, sep=" | ")

def scripted(history, tool_names):
    done = len(history) - 1                     # how many tool results so far
    if done == 0:
        return {"tool": "describe", "args": {"name": "aircondit"}}
    if done == 1:
        return {"tool": "boot_se", "args": {"name": "aircondit", "stat": "mean", "B": 2000}}
    se = history[-1].split("'se': ")[1].rstrip("}")
    return {"final": "Bootstrap SE of the mean: " + se}

out = run_agent(scripted, tools, "Estimate the mean failure time and its bootstrap standard error.")
print(out["answer"])

# Predict
show(out["receipt"])


## 3.2 An agent's success rate

rng = np.random.default_rng(5400)

def sloppy(history, tool_names):
    done = len(history) - 1
    u = rng.uniform()
    if done == 0:
        return {"tool": "describe", "args": {"name": "aircondit"}}
    if history[-1].startswith("boot_se: ERROR"):        # recover from an error
        return {"tool": "boot_se", "args": {"name": "aircondit", "stat": "mean", "B": 2000}}
    if done == 1:
        if u < 0.10:                                     # answers without bootstrapping
            return {"final": "Bootstrap SE of the mean: about 40."}
        if u < 0.25:                                     # the wrong statistic
            return {"tool": "boot_se", "args": {"name": "aircondit", "stat": "median", "B": 2000}}
        if u < 0.32:                                     # a typo in the statistic
            return {"tool": "boot_se", "args": {"name": "aircondit", "stat": "maen", "B": 2000}}
        return {"tool": "boot_se", "args": {"name": "aircondit", "stat": "mean", "B": 2000}}
    se = history[-1].split("'se': ")[1].rstrip("}")
    return {"final": "Bootstrap SE of the mean: " + se}

show(run_agent(sloppy, tools, "Estimate the mean failure time and its bootstrap SE.")["receipt"])


## 3.3 Success rate, with an interval

truth = boot_se("aircondit", "mean", B=2000, seed=5400)["se"]

def is_right(answer):
    try:
        return abs(float(answer.split(": ")[1]) - truth) < 0.05
    except Exception:
        return False

task = "Estimate the mean failure time and its bootstrap SE."
rng = np.random.default_rng(5400)
runs = [run_agent(sloppy, tools, task) for _ in range(200)]
ok = np.array([is_right(r["answer"]) for r in runs])
print(ok.mean())

# Wilson interval, by the formula from Section 3.2
n, p, z = len(ok), ok.mean(), 1.959964
center = (p + z**2 / (2 * n)) / (1 + z**2 / n)
half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / (1 + z**2 / n)
print(center - half, center + half)

steps, counts = np.unique([r["steps"] for r in runs], return_counts=True)
print(dict(zip(steps.tolist(), counts.tolist())))


## 3.4 Audit the agent

# By hand
receipt_1 = [
    (1, "describe", "{'name': 'aircondit'}", "12 values; mean 108.1; median 88.0"),
    (2, "boot_se",  "{'name': 'aircondit', 'stat': 'median', 'B': 2000}", "{'estimate': 88.0, 'se': 28.78}"),
    (3, "(answer)", "", "Bootstrap SE of the mean: 28.78")]
show(receipt_1)

# By hand
receipt_2 = [
    (1, "describe", "{'name': 'aircondit'}", "12 values; mean 108.1; median 88.0"),
    (2, "(answer)", "", "Bootstrap SE of the mean: 39.3 (the standard deviation divided by the square root of 12)")]
show(receipt_2)

# By hand
receipt_3 = [
    (1, "describe", "{'name': 'aircondit'}", "12 values; mean 108.1; median 88.0"),
    (2, "boot_se",  "{'name': 'aircondit', 'stat': 'mean', 'B': 2000, 'seed': 5400}", "{'estimate': 108.1, 'se': 36.77}"),
    (3, "boot_se",  "{'name': 'aircondit', 'stat': 'mean', 'B': 2000, 'seed': 5400}", "{'estimate': 108.1, 'se': 36.77}"),
    (4, "(answer)", "", "Bootstrap SE of the mean: 36.77, confirmed by two independent bootstrap runs.")]
show(receipt_3)
