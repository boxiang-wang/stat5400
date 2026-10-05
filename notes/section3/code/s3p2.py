# STAT:5400 Section 3.2 — CLT and Confidence Intervals
# Code from the lecture notes; no output, no solutions.

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


## 1.4 One dimension, four sample sizes

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(5400)
n = np.repeat([10, 25, 40, 100], 100)
y = np.array([np.mean(np.random.normal(size=k)) for k in n])

# same picture with matplotlib: jitter the rows by hand
jitter = np.random.uniform(-0.15, 0.15, len(n))
level = np.searchsorted([10, 25, 40, 100], n)    # 0, 1, 2, 3
plt.scatter(y, level + jitter, s=8, color="black")
plt.yticks(range(4), ["10", "25", "40", "100"])
plt.xlabel("sample mean"); plt.ylabel("sample size")
plt.show()


## 1.6 Simulating the sampling distribution

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(5400)
n = 30           # sample size
mu = 1           # population mean
sig_sq = 4       # population variance

# generating 1000 random samples,
#   each of which is of size 30.
# record the 1000 sample means.
Xbarlist = np.full(1000, np.nan)
for i in range(1000):
    Xlist = np.random.normal(mu, np.sqrt(sig_sq), n)
    Xbarlist[i] = np.mean(Xlist)

# a faster way
np.random.seed(5400)
n = 30           # sample size
mu = 1           # population mean
sig_sq = 4       # population variance

Xlist = np.random.normal(mu, np.sqrt(sig_sq), (1000, n))
Xbarlist = Xlist.mean(axis=1)     # row means

plt.hist(Xbarlist)
plt.show()


## 1.7 Functions `qqnorm` and `qqline` in R

import scipy.stats

scipy.stats.probplot(Xbarlist, plot=plt)
plt.show()


## 1.9 Four sample sizes

np.random.seed(5400)
Xbar1 = [np.mean(np.random.normal(mu, sig_sq**0.5, 10)) for i in range(1000)]
Xbar2 = [np.mean(np.random.normal(mu, sig_sq**0.5, 25)) for i in range(1000)]
Xbar3 = [np.mean(np.random.normal(mu, sig_sq**0.5, 50)) for i in range(1000)]
Xbar4 = [np.mean(np.random.normal(mu, sig_sq**0.5, 100)) for i in range(1000)]

fig, axs = plt.subplots(2, 2)
fig.suptitle('Histogram of sample mean of normal dist')
axs[0, 0].hist(Xbar1); axs[0, 0].set_title('n = 10')
axs[0, 1].hist(Xbar2); axs[0, 1].set_title('n = 25')
axs[1, 0].hist(Xbar3); axs[1, 0].set_title('n = 50')
axs[1, 1].hist(Xbar4); axs[1, 1].set_title('n = 100')
for ax in axs.flat:
    ax.set(xlabel='Xbarlist', ylabel='Frequency')
for ax in axs.flat:
    ax.label_outer()
plt.show()


## 2.2 CLT for random samples drawn from the uniform

np.random.seed(5400)
fig, axs = plt.subplots(2, 2)
for ax, nlist in zip(axs.flat, [5, 10, 20, 30]):
    Xlist = np.random.uniform(size=(1000, nlist))
    Xbarlist = Xlist.mean(axis=1)
    ax.hist(Xbarlist)
    ax.set_xlim(0, 1)
    ax.set_title(f"Histogram of sample mean: n = {nlist}", fontsize=8)
fig.tight_layout()
plt.show()

np.random.seed(5400)
fig, axs = plt.subplots(2, 2)
for ax, nlist in zip(axs.flat, [5, 10, 20, 30]):
    Xlist = np.random.uniform(size=(1000, nlist))
    Xbarlist = Xlist.mean(axis=1)
    scipy.stats.probplot(Xbarlist, plot=ax)
    ax.set_title(f"Q-Q plot of sample mean: n = {nlist}", fontsize=8)
fig.tight_layout()
plt.show()


## 2.3 CLT for random samples drawn from the exponential

np.random.seed(5400)
fig, axs = plt.subplots(2, 2)
for ax, nlist in zip(axs.flat, [5, 10, 20, 50]):
    Xlist = np.random.exponential(1, (1000, nlist))
    Xbarlist = Xlist.mean(axis=1)
    ax.hist(Xbarlist)
    ax.set_xlim(0, 3)
    ax.set_title(f"Histogram of sample mean: n = {nlist}", fontsize=8)
fig.tight_layout()
plt.show()

np.random.seed(5400)
fig, axs = plt.subplots(2, 2)
for ax, nlist in zip(axs.flat, [5, 10, 20, 50]):
    Xlist = np.random.exponential(1, (1000, nlist))
    Xbarlist = Xlist.mean(axis=1)
    scipy.stats.probplot(Xbarlist, plot=ax)
    ax.set_title(f"Q-Q plot of sample mean: n = {nlist}", fontsize=8)
fig.tight_layout()
plt.show()


## 2.4 Application: a model's accuracy is a sample mean

import matplotlib.pyplot as plt
np.random.seed(5400)
theta = 0.88
fig, axes = plt.subplots(1, 3, figsize=(10, 3))
for ax, n in zip(axes, [25, 100, 1000]):
    acc = np.random.binomial(n, theta, 10000) / n     # accuracy on 10,000 test sets
    ax.hist(acc, bins=20)
    ax.set_xlim(0.7, 1); ax.set_title(f"n = {n}"); ax.set_xlabel("Accuracy")
plt.show()

n = np.array([100, 500, 1000, 5000])
print(np.round(scipy.stats.norm.ppf(0.975) * np.sqrt(theta * (1 - theta) / n), 3))


## 3.2 Getting the quantile

import scipy.stats

print(-scipy.stats.norm.ppf(0.025))
print(scipy.stats.norm.cdf(1.96))

x = np.linspace(-3, 3, 301)
plt.plot(x, scipy.stats.norm.pdf(x), color="black", lw=3)
plt.title("Probability Density Function of N(0,1)")
plt.xlabel("X"); plt.ylabel("f(x)")
cord_x = np.arange(scipy.stats.norm.ppf(0.975), 3, 0.01)
plt.fill_between(cord_x, scipy.stats.norm.pdf(cord_x), color="skyblue")
plt.annotate(r"$\alpha/2$", xy=(2.5, 0.01), xytext=(2.7, 0.09),
             arrowprops=dict(arrowstyle="->"))
plt.xticks([-3, -2, -1, 0, 1, scipy.stats.norm.ppf(0.975), 3],
           ["-3", "-2", "-1", "0", "1", r"$z_{\alpha/2}$", "3"])
plt.axhline(0, color="black")
plt.show()


## 3.4 Coverage probability of a random confidence interval

np.random.seed(5400)
n = 20
alp = 0.05
sig_sq = 1
mu = 0.5
Xlist = [np.random.normal(mu, sig_sq**0.5, n) for i in range(10000)]
Xbarlist = np.mean(Xlist, 1)

cri = scipy.stats.norm.ppf(1 - alp/2)
moe = cri * (sig_sq / n)**0.5
print(np.mean([(mu > Xbarlist[i] - moe and mu < Xbarlist[i] + moe)
  for i in range(10000)]))


## 3.5 Case II: unknown variance, normality

x = np.linspace(-3, 3, 301)
plt.plot(x, scipy.stats.norm.pdf(x), color="black", lw=3, label="normal")
plt.plot(x, scipy.stats.t.pdf(x, 1), "--", color="red", label="t(1)")
plt.plot(x, scipy.stats.t.pdf(x, 2), ":", color="blue", label="t(2)")
plt.plot(x, scipy.stats.t.pdf(x, 5), "-.", color="green", label="t(5)")
plt.plot(x, scipy.stats.t.pdf(x, 50), linestyle=(0, (5, 5)), color="brown", label="t(50)")
plt.axhline(0, color="black")
plt.title("Normal and t"); plt.xlabel("X"); plt.ylabel("f(x)")
plt.legend(loc="upper right")
plt.show()

# By hand
# case II true dist: N(0.5, 1)
np.random.seed(5400)
n = 20; alp = 0.05; mu = 0.5; sig_sq = 1
Xlist = np.random.normal(mu, np.sqrt(sig_sq), (10000, n))
Xbarlist = Xlist.mean(axis=1)
sdlist = Xlist.std(axis=1, ddof=1)

se = 0                        # <- change this line

CI = np.c_[Xbarlist - se, Xbarlist + se]
is_cover = (mu > CI[:, 0]) & (mu < CI[:, 1])
print(np.mean(is_cover))


## 3.6 Case III: non-normality, large sample

# By hand
# case III true dist: exp with mean 2
np.random.seed(5400)
n = 20; alp = 0.05; mu = 2
Xlist = np.random.exponential(mu, (10000, n))    # scale = mean
Xbarlist = Xlist.mean(axis=1)
sdlist = Xlist.std(axis=1, ddof=1)

moe = 0                       # <- change this line

CI = np.c_[Xbarlist - moe, Xbarlist + moe]
is_cover = (mu > CI[:, 0]) & (mu < CI[:, 1])
print(np.mean(is_cover))


## 3.7 How large is large enough?

def CovProb(n, mu=2, alp=0.05):
    Xlist = [np.random.exponential(mu, n) for i in range(10000)]
    Xbarlist = np.mean(Xlist, 1)
    Slist = np.std(Xlist, 1, ddof=1)
    moe = scipy.stats.norm.ppf(1 - alp/2) * Slist / n**0.5
    return np.mean([(mu > Xbarlist[i] - moe[i] and
                     mu < Xbarlist[i] + moe[i])
                    for i in range(10000)])

np.random.seed(5400)
print(CovProb(10))
print(CovProb(30))
print(CovProb(50))
print(CovProb(200))


## 3.8 Application: how long an AI model takes to answer

def CovProbLN(n, meanlog=0, sdlog=1.2, alp=0.05):
    mu = np.exp(meanlog + sdlog**2 / 2)       # true mean latency
    Xlist = np.random.lognormal(meanlog, sdlog, (10000, n))
    Xbarlist = Xlist.mean(axis=1)
    Slist = Xlist.std(axis=1, ddof=1)
    moe = scipy.stats.norm.ppf(1 - alp/2) * Slist / n**0.5
    return np.mean((Xbarlist - moe < mu) & (mu < Xbarlist + moe))

np.random.seed(5400)
print([CovProbLN(n) for n in [10, 30, 100, 200]])


## 3.10 Generating dependent samples

rho = 0.1; n = 5
Sigma = np.full((n, n), rho)
np.fill_diagonal(Sigma, 1)
values, vectors = np.linalg.eigh(Sigma)    # eigh: for symmetric matrices
Sigma_sq = vectors @ np.diag(np.sqrt(values)) @ vectors.T

print(Sigma_sq @ Sigma_sq)

np.random.seed(5400)
X = np.random.normal(size=n) @ Sigma_sq
print(X)

np.random.seed(5400)
bigN = 10**4  # 1e4 keeps this quick in the browser; try 1e5 on your own computer
Xlist = np.random.normal(0, 1, (bigN, n)) @ Sigma_sq
print(np.round(np.cov(Xlist, rowvar=False), 3))    # rowvar=False: columns are variables


## 3.11 Coverage as $\rho$ varies

# bigN = 1e4 keeps the 20-point curve quick in the browser; try 1e5 on your own computer
def CovProb2(rho, n=30, mu=0, bigN=10**4, alp=0.05):
    Sigma = np.full((n, n), rho)
    np.fill_diagonal(Sigma, 1)
    values, vectors = np.linalg.eigh(Sigma)
    Sigma_sq = vectors @ np.diag(np.sqrt(values)) @ vectors.T
    # generate dependent samples
    Xlist = mu + np.random.normal(size=(bigN, n)) @ Sigma_sq
    Xbarlist = Xlist.mean(axis=1)
    moe = scipy.stats.norm.ppf(1 - alp/2) * 1 / np.sqrt(n)
    CI = np.c_[Xbarlist - moe, Xbarlist + moe]
    is_cover = (mu > CI[:, 0]) & (mu < CI[:, 1])
    return np.mean(is_cover)

# Predict
np.random.seed(5400)
rhos = np.linspace(0, 0.1, 20)
covprobs = np.full(20, np.nan)
for i in range(20):
    # call the function above
    covprobs[i] = CovProb2(rhos[i])

plt.plot(rhos, covprobs, "o-")
plt.xlabel(r"$\rho$"); plt.ylabel("Coverage Probabilities")
plt.show()

np.random.seed(5400)
covprobs = [CovProb2(r) for r in rhos]
print(np.round(covprobs[:6], 4))

covprobs = np.full(20, np.nan)
for i in range(20):
    covprobs[i] = CovProb2(rhos[i])


## 3.12 Application: benchmark questions that come in groups

def CovClust(K=40, m=5, B=2000):
    naive = np.zeros(B, bool); passage = np.zeros(B, bool)
    for r in range(B):
        pk = np.random.choice([0.9, 0.5], K)                           # each passage is easy or hard
        Y = np.random.binomial(1, np.repeat(pk[:, None], m, axis=1))   # row = passage
        se_naive = Y.std(ddof=1) / np.sqrt(K * m)                      # treats all answers as independent
        se_passage = Y.mean(axis=1).std(ddof=1) / np.sqrt(K)           # uses the K passage means
        naive[r] = abs(Y.mean() - 0.7) < 1.96 * se_naive
        passage[r] = abs(Y.mean() - 0.7) < 1.96 * se_passage
    return naive.mean(), passage.mean()

np.random.seed(5400)
print(CovClust())


## 4.3 Comparing the six

np.random.seed(5400)
theta = 0.6
n = 40
B = 1000        # 1000 keeps this quick in the browser; try B = 10000 on your own computer
alp = 0.05
# generate data
Xbarlist = np.random.binomial(n, theta, B) / n

## Wald interval
moe_Wald = scipy.stats.norm.ppf(1 - alp/2) * np.sqrt(Xbarlist * (1 - Xbarlist) / n)
CI_Wald = np.c_[Xbarlist - moe_Wald, Xbarlist + moe_Wald]
## simple conservative interval
moe_simple = scipy.stats.norm.ppf(1 - alp/2) * np.sqrt(0.5 * (1 - 0.5) / n)
CI_simple = np.c_[Xbarlist - moe_simple, Xbarlist + moe_simple]

## score, CP, AC, and the Jeffreys Bayesian CIs
# no loop: each interval is computed for all B samples at once from its formula
z = scipy.stats.norm.ppf(1 - alp/2)
x = np.round(n * Xbarlist)                       # number of successes
## score (Wilson)
ctr = (x + 0.5 * z**2) / (n + z**2)
moe_score = z * np.sqrt(x * (1 - x/n) + 0.25 * z**2) / (n + z**2)
CI_score = np.c_[ctr - moe_score, ctr + moe_score]
## Clopper-Pearson, written with beta quantiles (same as the F form)
CI_CP = np.c_[scipy.stats.beta.ppf(alp/2, x, n - x + 1),
              scipy.stats.beta.ppf(1 - alp/2, x + 1, n - x)]
CI_CP[x == 0, 0] = 0; CI_CP[x == n, 1] = 1
## Agresti-Coull
p_hat = (x + z**2 / 2) / (n + z**2)
moe_AC = z * np.sqrt(p_hat * (1 - p_hat) / (n + z**2))
CI_AC = np.c_[p_hat - moe_AC, p_hat + moe_AC]
## Jeffreys: quantiles of the Beta(x + 1/2, n - x + 1/2) posterior
CI_Bayes = np.c_[scipy.stats.beta.ppf(alp/2, x + 0.5, n - x + 0.5),
                 scipy.stats.beta.ppf(1 - alp/2, x + 0.5, n - x + 0.5)]

## get mean and se of width and coverage probability
def width_cov(CI):
    w = CI[:, 1] - CI[:, 0]                             # width
    cov = (theta > CI[:, 0]) & (theta < CI[:, 1])       # coverage
    return [w.mean(), w.std(ddof=1) / np.sqrt(len(w)),
            cov.mean(), cov.std(ddof=1) / np.sqrt(len(cov))]

## display results
col_nm = ["CI_simple", "CI_Wald", "CI_score", "CI_CP", "CI_AC", "CI_Bayes"]
res = np.column_stack([width_cov(CI) for CI in
                       [CI_simple, CI_Wald, CI_score, CI_CP, CI_AC, CI_Bayes]])
print(col_nm)
for name, row in zip(["exp.width", "se", "cov.prob", "se"], np.round(res, 3)):
    print(name, row)


## 4.4 Application: asking a model the same question 50 times

res = scipy.stats.binomtest(22, 50)     # 22 correct answers in 50 runs
print(res.proportion_ci(method="wilson"))
print(res.proportion_ci(method="exact"))

import json, urllib.request
from collections import Counter

q = "Which is larger, 9.9 or 9.11? Answer with the number only."
answers = [""] * 50
for i in range(50):                                            # a new chat each time
    req = urllib.request.Request("http://localhost:11434/api/chat",
        data=json.dumps({"model": "llama3.2:1b", "stream": False,
                         "messages": [{"role": "user", "content": q}]}).encode(),
        headers={"Content-Type": "application/json"})
    answers[i] = json.load(urllib.request.urlopen(req))["message"]["content"].strip()
print(Counter(answers))
