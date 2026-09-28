# STAT:5400 Section 3.1 — Random Number Generators
# Code from the lecture notes; no output, no solutions.

## 2.1 Draw from the uniform distribution

import numpy as np

u = np.random.uniform(0, 1, 1)
print(u)


## 2.2 Set seed

np.random.seed(5400)
u = np.random.uniform(0, 1, 1)
print(u)

np.random.seed(5400)
state = np.random.get_state()   # ("MT19937", 624 integers, position, ...)
print(len(state[1]))
print(state[1][:6])


## 2.3 Generate $U \sim \mathrm{Unif}(1, 5)$

# Predict
np.random.seed(5400)
u1 = np.random.uniform(1, 5, 1)
print(u1)

# Predict
np.random.seed(5400)
u2 = np.random.uniform(0, 1, 1) * 4 + 1
print(u2)

# Predict
help(np.random.uniform)


## 2.5 Generating many uniforms

np.random.seed(5400)
ulist = np.random.uniform(1, 5, 5)
print(ulist)

np.random.seed(5400)
ulist = np.full(5, np.nan)
for i in range(5):
    ulist[i] = np.random.uniform(1, 5)
print(ulist)


## 2.6 R and Python do not share a stream

import numpy as np

np.random.seed(5400)
print(4 * np.random.uniform(0, 1, 1) + 1)

np.random.seed(5400)
print(np.random.uniform(1, 5, 5))


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


## 2.12 Q-Q plot (quantile-quantile plot)

import scipy.stats
import matplotlib.pyplot as plt

np.random.seed(5400)
ulist = np.random.uniform(0, 1, 1000)
probs = (np.arange(1, 1001) - 0.5) / 1000   # same as ppoints(1000) in R
plt.scatter(scipy.stats.uniform.ppf(probs), np.sort(ulist), s=8)
plt.axline((0, 0), slope=1, color="black")
plt.xlabel("Theoretical Quantiles")
plt.ylabel("Sample Quantiles")
plt.title("Q-Q plot")
plt.show()


## 3.1 Drawing from Bernoulli distribution

import numpy as np

# Generate Bern(0.4)
Y = (np.random.uniform(0, 1, 1) < 0.4).astype(float)
print(Y)

np.random.seed(5400)
# Generate Y1, ..., Y100 ~ Bern(0.4)
Ylist = (np.random.uniform(0, 1, 100) < 0.4).astype(float)

# population mean is 0.4
print(np.mean(Ylist))

# population variance is 0.4 * 0.6 = 0.24
print(np.var(Ylist, ddof=1))   # ddof=1 divides by n - 1, like R's var


## 3.2 Drawing from Binomial distribution

np.random.seed(5400)
# Generate X ~ Bin(100, 0.4)
X = np.sum(np.random.uniform(0, 1, 100) < 0.4)
print(X)

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


## 4.3 Histogram against the density

# By hand
import scipy.stats
import matplotlib.pyplot as plt

plt.subplot(1, 2, 1)
plt.hist(Xlist)
xs = np.linspace(0.001, 12, 200)
plt.subplot(1, 2, 2)
plt.plot(xs, scipy.stats.expon.pdf(xs, scale=1))   # <- change this line
plt.ylim(0, 1)
plt.xlabel("X")
plt.ylabel("f(x)")
plt.title("exp(2)")
plt.show()


## 4.4 Q-Q plot for the exponential

# By hand
probs = (np.arange(1, 1001) - 0.5) / 1000   # same as ppoints(1000) in R
plt.scatter(probs, np.full(1000, 0.5), s=8)  # <- change this line
plt.axline((0, 0), slope=1, color="black")
plt.xlabel("Theoretical Quantiles")
plt.ylabel("Sample Quantiles")
plt.title("Q-Q plot for exponential distribution")
plt.show()


## 4.5 The `rexp` function in R

np.random.seed(5400)
Xlist = np.random.exponential(scale=2, size=1000)   # scale is the mean
print(Xlist[0:3])

print(np.mean(Xlist))
print(np.var(Xlist, ddof=1))

# Predict
np.random.seed(5400)
print(-2 * np.log(np.random.uniform(0, 1, 3)))
np.random.seed(5400)
print(np.random.exponential(scale=2, size=3))


## 4.6 Drawing from the standard Cauchy distribution

np.random.seed(5400)
# Generate X1, ..., X1000 ~ Cauchy
Ulist = np.random.uniform(0, 1, 1000)
Xlist = np.tan(np.pi * (Ulist - 0.5))

import scipy.stats
import matplotlib.pyplot as plt

plt.subplot(1, 2, 1)
plt.hist(Xlist)
xs = np.linspace(-10, 10, 200)
plt.subplot(1, 2, 2)
plt.plot(xs, scipy.stats.cauchy.pdf(xs))
plt.ylim(0, 1)
plt.xlabel("X")
plt.ylabel("f(x)")
plt.title("PDF of Cauchy distribution")
plt.show()

# By hand
probs = (np.arange(1, 1001) - 0.5) / 1000   # same as ppoints(1000) in R
plt.scatter(probs, np.full(1000, 0.5), s=8)  # <- change this line
plt.axline((0, 0), slope=1, color="black")
plt.xlabel("Theoretical Quantiles")
plt.ylabel("Sample Quantiles")
plt.title("Q-Q plot for Cauchy distribution")
plt.show()


## 4.7 Cauchy and $t$

np.random.seed(5400)
print(np.mean(np.random.standard_cauchy(10000)))
print(np.mean(np.random.standard_cauchy(10000)))
print(np.mean(np.random.standard_cauchy(10000)))


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

Rsq = np.array([row[0]**2 + row[1]**2 for row in V])
ok = Rsq > 0                # drop a pair that is exactly (0, 0)
m = np.sqrt(-(2 * np.log(Rsq[ok])) / Rsq[ok])
x = m[:, None] * np.array(V)[ok]


## 6.3 Checking the normals

import scipy.stats
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 2)
# histograms
ax[0, 0].hist(x[:, 0])
ax[0, 0].set_title("Histogram of X1")
ax[0, 1].hist(x[:, 1])
ax[0, 1].set_title("Histogram of X2")
# Q-Q plots
probs = (np.arange(1, len(x) + 1) - 0.5) / len(x)   # same as ppoints(NROW(X)) in R
ax[1, 0].scatter(scipy.stats.norm.ppf(probs), np.sort(x[:, 0]), s=8)
ax[1, 0].axline((0, 0), slope=1, color="black")
ax[1, 0].set_title("Q-Q plot for X1")
ax[1, 1].scatter(scipy.stats.norm.ppf(probs), np.sort(x[:, 1]), s=8)
ax[1, 1].axline((0, 0), slope=1, color="black")
ax[1, 1].set_title("Q-Q plot for X2")
plt.tight_layout()
plt.show()


## 6.4 Q-Q plot for $\mathrm{N}(\mu, \sigma^2)$

newx = x[:, 0] * 2 + 4
dat_quant = np.sort(newx)
thr_quant = scipy.stats.norm.ppf((np.arange(1, len(newx) + 1) - 0.5) / len(newx))
plt.scatter(thr_quant, dat_quant, s=8)
plt.axline((0, 4), slope=2, color="black")   # intercept 4, slope 2
plt.xlabel("Theoretical Quantiles")
plt.ylabel("Sample Quantiles")
plt.title("Q-Q plot for X ~ N(4, 4)")
plt.show()


## 6.5 `qqnorm` and `qqline`

import scipy.stats
import matplotlib.pyplot as plt

newx = np.array(x)[:, 1] * 2 + 4
fig, ax = plt.subplots(1, 1)
scipy.stats.probplot(newx, plot=plt)
plt.show()


## 6.6 What R actually uses

np.random.seed(5400)
print(scipy.stats.norm.ppf(np.random.uniform(0, 1, 1)))

np.random.seed(5400)
# np.random.normal uses the polar method above, not inversion,
# so this number is different from the one in the block above
print(np.random.normal(0, 1, 1))


## 6.7 Standard Cauchy, again

V_arr = np.array(V)
Y = V_arr[:, 0] / V_arr[:, 1]
# min, 1st quartile, median, 3rd quartile, max, then the mean
print(np.percentile(Y, [0, 25, 50, 75, 100]))
print(np.mean(Y))


## 6.8 $\chi_v^2$ distribution

np.random.seed(5400)
Zlist = np.random.normal(0, 1, 10)
Y = np.sum(Zlist**2)
print(Y)


## 6.9 Student's $t$ distribution

import scipy.stats
import matplotlib.pyplot as plt

xs = np.linspace(-3, 3, 200)
plt.plot(xs, scipy.stats.norm.pdf(xs, 0, 1), lw=3, ls="-", color="black", label="normal")
plt.plot(xs, scipy.stats.t.pdf(xs, 1), ls="--", color="red", label="t(1)")
plt.plot(xs, scipy.stats.t.pdf(xs, 2), ls=":", color="blue", label="t(2)")
plt.plot(xs, scipy.stats.t.pdf(xs, 5), ls="-.", color="green", label="t(5)")
plt.axhline(0, color="black")
plt.xlabel("X")
plt.ylabel("f(x)")
plt.title("Normal and t")
plt.legend(loc="upper right")
plt.show()


## 7.4 Generate one copy from $\mathrm{N}_p(\boldsymbol{\mu}, \boldsymbol{\Sigma})$

import numpy as np

np.random.seed(5400)
# sample size and dimension
n = 1000
p = 5
# var-covariance matrix
Sigma = np.full((p, p), 0.5)
np.fill_diagonal(Sigma, 1)
mu = np.arange(1, p + 1)   # mean vector

# eigen-decomposition (eigh is for symmetric matrices)
eig_values, eig_vectors = np.linalg.eigh(Sigma)
Sigma_sqrt = eig_vectors @ np.diag(np.sqrt(eig_values)) @ eig_vectors.T

Z = np.random.normal(0, 1, p)
X = mu + Sigma_sqrt @ Z
print(X)


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


## 7.6 `mvtnorm` in R and `multivariate_normal` in Python

np.random.seed(5400)
Z = np.random.normal(0, 1, p)
X = mean + Z @ sigma_sqrt
print(X[0:2])

from scipy.stats import multivariate_normal

np.random.seed(5400)
d = multivariate_normal(mean=mean, cov=sigma)
X = d.rvs(1)
print(X[0:2])
