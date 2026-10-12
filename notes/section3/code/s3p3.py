# STAT:5400 Section 3.3 — Hypothesis Testing and Replicates
# Code from the lecture notes; no output, no solutions.

## 1.4 The observed $p$-value

import numpy as np
import scipy.stats

np.random.seed(5400)
n    = 30
mu   = 1
mu_0 = 1
sig  = 2
alp  = 0.05
X = np.random.normal(mu, sig, n)

t_stat = (np.mean(X) - mu_0) / (np.std(X, ddof=1) / n**0.5)
print(t_stat)

p_val = 2 * scipy.stats.t.cdf(-np.abs(t_stat), n - 1)
print(p_val)


## 1.7 The function `pvalDist`

"""Simulation of p-values

The function is used to simulate
  the distribution of observed p-values

Parameters
    n      sample size
    mu     true mean
    mu_0   mean to be tested
    sig    true standard deviation
    alp    significance level, default is 0.05
    B      simulation size, default is 10000
Returns
    a list of observed pvals
"""

def pvalDist(n, mu, mu_0, sig, alp=0.05, B=10000):
    Xlist = [np.random.normal(mu, sig, n) for i in range(B)]
    Xbarlist = np.mean(Xlist, 1)
    Slist = np.std(Xlist, 1, ddof=1)
    t_stat_list = (Xbarlist - mu_0) / (Slist / n**0.5)
    pvals = 2 * scipy.stats.t.sf(np.abs(t_stat_list), n - 1)   # all B p-values at once
    return pvals


## 1.8 Type I error when $H_0$ is true

np.random.seed(5400)
n    = 30
mu   = 1
mu_0 = 1
sig  = 2
alp  = 0.05

pvals = pvalDist(n, mu, mu_0, sig, alp)
print(np.mean([pvals[i] < alp for i in range(10000)]))

import matplotlib.pyplot as plt

# Q-Q plot for uniform distribution
def qqunif(dat, **kwargs):
    probs = (np.arange(1, len(dat) + 1) - 0.5) / len(dat)   # ppoints(length(dat))
    plt.plot(scipy.stats.uniform.ppf(probs), np.sort(dat), 'o', mfc='none', **kwargs)
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Sample Quantiles")
    plt.title("Q-Q plot")
    plt.plot([0, 1], [0, 1], 'k-')                          # abline(0, 1)

# Histogram and Q-Q plot for observed p-value
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.hist(pvals, edgecolor='black')
plt.title("Histogram of observed p-val")
plt.xlabel("Observed p-values")
plt.subplot(1, 2, 2)
qqunif(pvals)
plt.show()


## 1.9 Application: trying many prompts and keeping the best

np.random.seed(5400)
K = [1, 5, 20]
print([np.mean(np.random.rand(5000, k).min(axis=1) < 0.05) for k in K])
print([1 - 0.95**k for k in K])

np.random.seed(5400)
K = 20; n = 200
acc = np.random.binomial(n, 0.70, K) / n               # observed accuracy of each prompt
print(acc.max())                                       # the best-looking prompt
print(1 - scipy.stats.norm.cdf((acc.max() - 0.70) / np.sqrt(0.70 * 0.30 / n)))
print(np.random.binomial(n, 0.70) / n)                 # the same prompt on 200 new questions


## 1.10 Power when $H_0$ is false

np.random.seed(5400)
n    = 30
mu   = 2
mu_0 = 1
sig  = 2
alp  = 0.05

pvals2 = pvalDist(n, mu, mu_0, sig, alp)
print(np.mean([pvals2[i] < alp for i in range(10000)]))

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.hist(pvals2, edgecolor='black')
plt.title("Histogram of observed p-val")
plt.xlabel("Observed p-values")
plt.subplot(1, 2, 2)
qqunif(pvals2)
plt.show()


## 1.11 Power curve under different sample sizes

np.random.seed(5400)
mu   = 2
mu_0 = 1
sig  = 2
alp  = 0.05

# compute the rejection probs
x = list(range(5, 51, 3))
rejprobs = [None] * len(x)

for i in range(len(x)):
    pvals = pvalDist(x[i], mu, mu_0, sig, alp, B=2000)
    rejprobs[i] = np.mean([p < alp for p in pvals])

import matplotlib.pyplot as plt

plt.plot(x, rejprobs, '-o')
plt.xlabel("Sample Sizes")
plt.ylabel("Prob of Rej H0")
plt.show()


## 1.12 Power curve under different true means

# By hand
np.random.seed(5400)
n      = 30
mulist = np.linspace(1, 3, 21)           # seq(1, 3, 0.1)
sig    = 2
alp    = 0.05
mu_0   = 1

rejprobs = [0.5] * len(mulist)           # <- change this line (a list comprehension)

plt.plot(mulist, rejprobs, '-o')
plt.xlabel("True Mean")
plt.ylabel("Prob of Rej H0")
plt.show()


## 1.13 Application: detecting text from a watermarked model

def wm_z(green, gamma=0.5):                # green: one 0/1 entry per token
    T = len(green)
    return (green.sum() - gamma * T) / np.sqrt(T * gamma * (1 - gamma))

np.random.seed(5400)
human = np.random.binomial(1, 0.5, 100)   # 100 tokens written by a person
model = np.random.binomial(1, 0.7, 100)   # 100 tokens from a watermarked model: 70% green
print(wm_z(human), wm_z(model))
print(1 - scipy.stats.norm.cdf(4))        # Type I error of the rule z > 4

np.random.seed(5400)
Tlist = np.arange(10, 301, 10)
power = [np.mean((np.random.binomial(T, 0.7, 2000) - 0.5 * T) / np.sqrt(T * 0.25) > 4)
         for T in Tlist]
plt.plot(Tlist, power, '-o')
plt.xlabel("Number of tokens"); plt.ylabel("Prob of detecting the watermark")
plt.show()


## 1.15 What breaks when normality fails

def pvalDistExp(n, mu, mu_0, alp=0.05, B=10000):
    Xlist = [np.random.exponential(mu, n) for i in range(B)]
    Xbarlist = np.mean(Xlist, 1)
    Slist = np.std(Xlist, 1, ddof=1)
    t_stat_list = (Xbarlist - mu_0) / (Slist / (n**0.5))
    return 2 * scipy.stats.t.sf(np.abs(t_stat_list), n - 1)    # all B p-values at once

np.random.seed(5400)
r1 = pvalDistExp(10, mu=2, mu_0=2)
print(np.mean([p < 0.05 for p in r1]))


## 1.16 A generic version

"""Simulation of p-values

The function simulates the observed p-values
  under different underlying distributions

Parameters
    n         sample size
    dist      normal, exponential, uniform, gamma, etc (names in np.random)
    mu_0      mean to be tested
    alp       significance level, default is 0.05
    B         simulation size, default is 10000
    **kwargs  args passed to the dist function
Returns
    a list of observed pvals
"""

def pvalDist2(n, dist, mu_0, alp=0.05, B=10000, **kwargs):
    rng = getattr(np.random, dist)
    Xlist = [rng(size=n, **kwargs) for i in range(B)]
    Xbarlist = np.mean(Xlist, 1)
    Slist = np.std(Xlist, 1, ddof=1)
    t_stat_list = (Xbarlist - mu_0) / (Slist / (n**0.5))
    return 2 * scipy.stats.t.sf(np.abs(t_stat_list), n - 1)    # all B p-values at once

np.random.seed(5400)
r2 = pvalDist2(10, "exponential", mu_0=2, scale=2)
print(np.mean([p < 0.05 for p in r2]))

# By hand
np.random.seed(5400)
n      = 10
mulist = np.linspace(1, 3, 21)           # seq(1, 3, 0.1)
alp    = 0.05
mu_0   = 1

rejprobs = [0.5] * len(mulist)           # <- change this line (a list comprehension)

plt.plot(mulist, rejprobs, '-o')
plt.xlabel("True Means")
plt.ylabel("Prob of Rej H0")
plt.title("Power Curve With True Distribution Exp")
plt.show()


## 2.3 Example 1: normal distribution

np.random.seed(5400)
mu = mu_0 = 1 # H0 is true
n = 30; sig = 2; alp = 0.05
pval = pvalDist(n, mu, mu_0, sig, alp=alp, B=10000)
theta_est = np.mean(np.array(pval) < alp)
print(theta_est)

# 95% simple conservative CI
moe = scipy.stats.norm.ppf(0.975) * 0.5 / np.sqrt(10000)
CI = theta_est + moe * np.array([-1, 1])
print(CI)
print(np.diff(CI))

np.random.seed(5400)
mu = mu_0 = 1 # H0 is true
n = 30; sig = 2; alp = 0.05
m = 0.005   # moe of 95% CI is at most m
# replicates
B = int(np.ceil((scipy.stats.norm.ppf(0.975) * 0.5 / m)**2))
print(B)

B = 10000   # 38415 is slow in the browser; delete this line on your own computer
pval = pvalDist(n, mu, mu_0, sig, alp=alp, B=B)
# estimated Type I error rate
theta_est = np.mean(np.array(pval) < alp)
print(theta_est)

# 95% simple conservative CI
moe = scipy.stats.norm.ppf(0.975) * 0.5 / np.sqrt(B)
CI = theta_est + moe * np.array([-1, 1])
print(CI)
print(np.diff(CI))

# Wilson score CI, the same interval as prop.test(correct = FALSE)
res = scipy.stats.binomtest(k=int(np.sum(np.array(pval) < alp)), n=B)
print(res.proportion_ci(confidence_level=0.95, method='wilson'))


## 2.4 Example 2: exponential distribution

np.random.seed(5400)
mu = mu_0 = 1 # H0 is true
n = 30; alp = 0.05
m = 0.005   # moe of 95% CI is at most m
B = int(np.ceil((scipy.stats.norm.ppf(0.975) * 0.5 / m)**2))
B = 10000   # the formula gives 38415, which is slow in the browser; delete this line on your own computer
pval2 = pvalDist2(n, "exponential", mu_0, alp=alp, B=B, scale=mu)   # scale = mean = 1/rate
# estimated Type I error rate
theta_est2 = np.mean(np.array(pval2) < alp)
print(theta_est2)

# 95% simple conservative CI
moe = scipy.stats.norm.ppf(0.975) * 0.5 / np.sqrt(B)
print(theta_est2 + moe * np.array([-1, 1]))

# Wilson score CI, the same interval as prop.test(correct = FALSE)
res2 = scipy.stats.binomtest(k=int(np.sum(np.array(pval2) < alp)), n=B)
print(res2.proportion_ci(confidence_level=0.95, method='wilson'))


## 2.5 Application: is model A better than model B?

np.random.seed(5400)
n = 300
d = np.random.normal(size=n)                   # difficulty of each question
A = np.random.binomial(1, 1 / (1 + np.exp(-(1.0 + 2 * d))))
B = np.random.binomial(1, 1 / (1 + np.exp(-(1.3 + 2 * d))))
print(A.mean(), B.mean())
print(np.std(B - A, ddof=1) / np.sqrt(n),
      np.sqrt(np.var(A, ddof=1) / n + np.var(B, ddof=1) / n))
print(scipy.stats.ttest_1samp(B - A, 0).pvalue)   # paired: one-sample t-test on D

def powerAB(n, reps=1000):
    rej = 0
    for r in range(reps):
        d = np.random.normal(size=n)
        A = np.random.binomial(1, 1 / (1 + np.exp(-(1.0 + 2 * d))))
        B = np.random.binomial(1, 1 / (1 + np.exp(-(1.3 + 2 * d))))
        rej += scipy.stats.ttest_1samp(B - A, 0).pvalue < 0.05
    return rej / reps

np.random.seed(5400)
print([powerAB(n) for n in [100, 300, 500, 1000]])
