# STAT:5400 Section 3.1 — Random Number Generators
# Code from the lecture notes; no output, no solutions.

## 2.6 R and Python do not share a stream

import numpy as np

np.random.seed(5400)
print(4 * np.random.uniform(0, 1, 1) + 1)

np.random.seed(5400)
print(np.random.uniform(1, 5, 5))

import rpy2.robjects as robjects
ulist = robjects.r("""
set.seed(5400)
ulist <- runif(5, 1, 5)
""")
print(np.array(ulist))
# [4.86860625 4.40436475 4.62585277 2.63676882 4.37947794]


## 2.7 Mean and variance of uniform distribution

import numpy as np

np.random.seed(5400)
ulist = np.random.uniform(0, 1, 100)
print(np.mean(ulist))
print(np.var(ulist))

import scipy.stats

np.random.seed(5400)
ulist = scipy.stats.uniform.rvs(0, 1, 100)
print(ulist.mean())
print(ulist.var())

# Edit
np.var(ulist, ddof=1)


## 2.10 The probability integral transform, seen

import matplotlib.pyplot as plt
import scipy.stats

plt.subplot(1, 2, 1)
X = np.random.uniform(2, 5, 1000)
plt.hist(scipy.stats.uniform.cdf(X, loc=2, scale=3))
plt.title("Uniform CDF")
plt.subplot(1, 2, 2)
X = scipy.stats.norm.rvs(0, 1, 1000)
plt.hist(scipy.stats.norm.cdf(X, loc=0, scale=1))
plt.title("Normal CDF")
plt.show()


## 2.11 Uniform random number generators in Python

np.random.seed(5400)
print(np.random.uniform(low=2, high=5, size=3))

np.random.seed(5400)
print(scipy.stats.uniform.rvs(loc=2, scale=3, size=3))


## 3.2 Drawing from Binomial distribution

np.random.seed(5400)
print(np.random.binomial(n=100, p=0.4, size=1))
print(scipy.stats.binom.rvs(n=100, p=0.4, size=1))


## 4.2 Drawing from exponential distribution

np.random.seed(5400)
Ulist = np.random.uniform(0, 1, 1000)
Xlist = [-2 * np.log(u) for u in Ulist]
print(Xlist[0:3])

print(np.mean(Xlist))
print(np.var(Xlist))


## 4.8 Sampling the next word

import numpy as np
words = ["reject", "accept", "retain"]
p = np.array([0.665, 0.245, 0.090])

rng = np.random.default_rng(5400)
u = rng.random()
print(words[np.searchsorted(np.cumsum(p), u, side="right")])   # one uniform, one word

# 10,000 draws: the frequencies match p
u = rng.random(10000)
idx = np.searchsorted(np.cumsum(p), u, side="right")
print(np.bincount(idx) / 10000)


## 5.2 Accept/reject sampling (cont'd)

np.random.seed(5400)
n = 500  # total samples
# Each row is a pair of V1 and V2. n rows in total.
dat = [np.random.uniform(-1, 1, 2) for i in range(n)]
# Accept if V_1^2 + V_2^2 <= 1.
accept = [(dat[i][0]**2 + dat[i][1]**2) <= 1 for i in range(n)]
print(np.mean([int(x) for x in accept]), np.pi / 4)

# Accepted pairs of V1 and V2
V = [dat[i] for i in range(n) if accept[i]]
# Rejected pairs of V1 and V2
V_out = [dat[i] for i in range(n) if not accept[i]]

import matplotlib.pyplot as plt

v = np.arange(-np.pi, np.pi, 0.1)
plt.plot(np.sin(v), np.cos(v), linewidth=0.5)
plt.scatter([row[0] for row in V], [row[1] for row in V],
  color="blue", marker="^", s=8)
plt.scatter([row[0] for row in V_out], [row[1] for row in V_out],
  color="red", marker="o", s=8)
plt.axis('equal')
plt.show()

from scipy import stats, optimize
c_bound = -optimize.minimize_scalar(
  lambda x: -stats.norm.pdf(x) / stats.cauchy.pdf(x),
  bounds=(-3, 3), method="bounded").fun
print(c_bound)

xs = np.linspace(-6, 6, 400)
env = c_bound * stats.cauchy.pdf(xs)
tgt = stats.norm.pdf(xs)
plt.fill_between(xs, tgt, env, color="0.9")      # rejected
plt.plot(xs, env, lw=2, color="#b8860b", label="c g(x), Cauchy envelope")
plt.plot(xs, tgt, lw=2, color="black", label="f(x), standard normal")
plt.xlabel("x"); plt.ylabel("density"); plt.legend()
plt.show()

rng = np.random.default_rng(5400)
n = 10000
Y = rng.standard_cauchy(n)
U = rng.random(n)
keep = U <= stats.norm.pdf(Y) / (c_bound * stats.cauchy.pdf(Y))
print(keep.mean(), 1 / c_bound)

X = Y[keep]
plt.hist(X, bins=40, density=True)
xs = np.linspace(-4, 4, 200)
plt.plot(xs, stats.norm.pdf(xs), lw=2)
plt.show()


## 6.2 Polar method for the standard normal

import sys

Rsq = [row[0]**2 + row[1]**2 for row in V]
Rsq = np.array(Rsq) + sys.float_info.min
m = [np.sqrt(-(2 * np.log(x)) / x) for x in Rsq]
x = [m[i] * V[i] for i in range(len(V))]


## 6.5 `qqnorm` and `qqline`

import scipy.stats
import matplotlib.pyplot as plt

newx = np.array(x)[:, 1] * 2 + 4
fig, ax = plt.subplots(1, 1)
scipy.stats.probplot(newx, plot=plt)
plt.show()


## 7.5 Generate multiple copies from $\mathrm{N}_p(\boldsymbol{\mu}, \boldsymbol{\Sigma})$

import numpy as np

np.random.seed(5400)
n = 1000
p = 5
mean = [x + 1 for x in range(p)]
sigma = [[0.5 for i in range(p)] for j in range(p)]
for i in range(p):
    sigma[i][i] = 1

v, w = np.linalg.eigh(sigma)
sigma_sqrt = w @ np.diag([v[i]**0.5 for i in range(p)]) @ w.T
Z = np.random.normal(0, 1, n * p).reshape(n, p)
mean_v = np.tile(mean, (n, 1))
X = mean_v + Z @ sigma_sqrt

print(np.mean(X, 0))
print(np.cov(X.T))


## 7.7 Python function `multivariate_normal`

np.random.seed(5400)
Z = np.random.normal(0, 1, p)
X = mean + Z @ sigma_sqrt
print(X[0:2])

from scipy.stats import multivariate_normal

np.random.seed(5400)
d = multivariate_normal(mean=mean, cov=sigma)
X = d.rvs(1)
print(X[0:2])
