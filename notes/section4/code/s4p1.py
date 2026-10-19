# STAT:5400 Section 4.1 — Bootstrap and Jackknife
# Code from the lecture notes; no output, no solutions.

## 1.3 Datasets `law82` and `law`

import pandas as pd
import numpy as np

law = pd.read_csv("data/law.csv")
law82 = pd.read_csv("data/law82.csv")
import scipy.stats
law_GPA = law["GPA"].to_numpy()
law82_GPA = law82["GPA"].to_numpy()
print(law82.head())

sampled_school = law82.merge(law, on=["LSAT", "GPA"])["School"]
print(law82.assign(sampled=law82["School"].isin(sampled_school)).head())


## 1.4 Confidence interval for the population mean

n = len(law_GPA)
print(np.mean(law_GPA))
se = np.std(law_GPA, ddof=1) / np.sqrt(n)
print(se)
print(np.mean(law_GPA) + np.array([-1, 1]) * 2 * se)
print(np.mean(law82_GPA))


## 1.6 Confidence interval for the population median

print(np.median(law_GPA))
se = np.std(law_GPA, ddof=1) / np.sqrt(n) * np.sqrt(np.pi/2)
print(se)
print(np.median(law_GPA) + np.array([-1, 1]) * 2 * se)
print(np.median(law82_GPA))


## 1.8 One bootstrap sample

# Predict
np.random.seed(5400)
x = [0.3, 0.7, 1.2, 1.4, 2.1]                # original sample
print(np.median(x))                          # s(X)
boot_samp = np.random.choice(x, len(x))      # one bootstrap sample X*
print(boot_samp)
print(np.median(boot_samp))                  # s(X*)


## 1.11 A toy example

np.random.seed(5400)
x = [0.3, 0.7, 1.2, 1.4, 2.1]
print(np.median(x))

# Generate B bootstrap samples and replicates
boot_rep = []
n = len(x)
for i in range(200):
    boot_sample = np.random.choice(x, n)
    boot_rep.append(np.median(boot_sample))

print(np.std(boot_rep, ddof=1))

import matplotlib.pyplot as plt

np.random.seed(5400)
# one bootstrap sample per column, as in replicate()
boot_samp = np.random.choice(x, size=(len(x), 200))
boot_rep = np.median(boot_samp, axis=0)
print(np.std(boot_rep, ddof=1))
plt.hist(boot_rep, edgecolor='k')
plt.title("Histogram of Bootstrap Replications")
plt.show()


## 1.12 Example: `law82` and `law`

np.random.seed(5400)
B = 200
boot_samp = np.random.choice(law_GPA, size=(len(law_GPA), B))
boot_rep = np.median(boot_samp, axis=0)
print(np.std(boot_rep, ddof=1))

import matplotlib.pyplot as plt

plt.hist(boot_rep, edgecolor='k')
plt.title("Histogram of Bootstrap Replications")
plt.show()


## 1.13 R package `boot`

# what boot() does, by hand: draw an index vector i, then call the statistic
np.random.seed(5400)
def m(x, i):
    return np.median(x[i])

n = len(law_GPA)
boot_rep2 = np.array([m(law_GPA, np.random.randint(0, n, n)) for b in range(200)])
print(np.std(boot_rep2, ddof=1))


## 1.14 `bootstrap` function in `scipy.stats`

from scipy.stats import bootstrap

np.random.seed(5400)
data = (law_GPA.ravel(), )
print(bootstrap(data, np.median, n_resamples=200).standard_error)


## 1.15 True standard error of the sample median

np.random.seed(5400)
B = 200
real_samp = np.column_stack([np.random.choice(law82_GPA, 15, replace=True)
                             for b in range(B)])
samp_dist_median = np.median(real_samp, axis=0)
print(np.std(samp_dist_median, ddof=1))


## 2.4 Example 2 of empirical distribution

print(law_GPA)

print(np.mean(law_GPA < 3))


## 2.8 Example: correlation coefficient

print(law["LSAT"].corr(law["GPA"]))

np.random.seed(5400)
B = 200
n = law.shape[0]
boot_rep = []

for i in range(B):
    sample = law.sample(n=n, replace=True, axis=0)
    boot_rep.append(sample["LSAT"].corr(sample["GPA"]))

print(np.std(boot_rep, ddof=1))

import scipy.stats
from scipy.stats import bootstrap

law_GPA = np.array(law[["GPA"]]).ravel()
law_LSAT = np.array(law[["LSAT"]]).ravel()

def my_corr(dat1, dat2):
    return scipy.stats.pearsonr(dat1, dat2)[0]

np.random.seed(5400)
print(bootstrap(data=(law_GPA, law_LSAT), statistic=my_corr,
  vectorized=False, paired=True, n_resamples=200).standard_error)


## 2.9 Population sampling versus bootstrap sampling

import matplotlib.pyplot as plt

np.random.seed(5400)
B = 200
n = law.shape[0]
sample_cor = []
boot_cor = []
for i in range(B):
    sample = law82.sample(n=n, replace=True, axis=0)
    sample_cor.append(sample["LSAT"].corr(sample["GPA"]))
    bt = law.sample(n=n, replace=True, axis=0)
    boot_cor.append(bt["LSAT"].corr(bt["GPA"]))

plt.subplot(1, 2, 1)
plt.hist(sample_cor, edgecolor='k')
plt.xlabel("Random Samples from Population")
plt.subplot(1, 2, 2)
plt.hist(boot_cor, edgecolor='k')
plt.xlabel("Bootstrap")
plt.show()


## 3.1 Nonparametric and parametric bootstrap

np.random.seed(5400)
# column means and covariance, as plain arrays
mu = law[['LSAT', 'GPA']].mean().values
covmat = law[['LSAT', 'GPA']].cov().values
boot_par_cor = []

for i in range(200):
    sample = np.random.multivariate_normal(mu, covmat, 15)
    sample = pd.DataFrame(sample, columns=['LSAT', 'GPA'])
    boot_par_cor.append(sample["LSAT"].corr(sample["GPA"]))

print(np.std(boot_par_cor, ddof=1))

import matplotlib.pyplot as plt

np.random.seed(5400)
law_LSAT = law["LSAT"].to_numpy()
n = len(law_GPA)
idmat = np.random.randint(0, n, size=(200, n))
boot_np_cor = [np.corrcoef(law_LSAT[idx], law_GPA[idx])[0, 1] for idx in idmat]
breaks = np.linspace(0, 1, 11)
plt.subplot(1, 2, 1)
plt.hist(boot_np_cor, bins=breaks, edgecolor='k')
plt.xlabel("Nonparametric Bootstrap")
plt.subplot(1, 2, 2)
plt.hist(boot_par_cor, bins=breaks, edgecolor='k')
plt.xlabel("Parametric Bootstrap")
plt.show()


## 3.2 Standard error of the sample correlation coefficient

rhat = np.corrcoef(law_LSAT, law_GPA)[0, 1]
print(rhat)
print((1 - rhat**2) / np.sqrt(law.shape[0] - 3))


## 4.2 Bootstrap estimation of bias

np.random.seed(5400)
rhat = law["LSAT"].corr(law["GPA"])
print(rhat)

B = 200
n = law.shape[0]
boot_r = []
for i in range(B):
    bt = law.sample(n=n, replace=True, axis=0)
    boot_r.append(bt["LSAT"].corr(bt["GPA"]))

bias = np.mean(boot_r - rhat)
print(bias)

print(bias / np.std(boot_r, ddof=1))
print(2 * np.std(boot_r, ddof=1) / np.sqrt(200))


## 4.5 Application: the bias of the best of 20 prompts

# Predict
np.random.seed(5400)
K = 20; n = 200
Y = np.random.binomial(1, 0.70, size=(K, n))      # row k: prompt k on the 200 questions
theta_hat = Y.mean(axis=1).max()                  # accuracy of the best prompt
print(theta_hat)
idmat = np.random.randint(0, n, size=(2000, n))   # 2000 resamples of the questions
boot_t = np.array([Y[:, i].mean(axis=1).max() for i in idmat])
bias = boot_t.mean() - theta_hat                  # bootstrap estimate of bias
print(bias, bias / np.std(boot_t, ddof=1))


## 5.1 Jackknife estimate of bias

np.random.seed(5400)
rhat = law["LSAT"].corr(law["GPA"])
n = law.shape[0]
jack_r = []

for i in range(n):
    dt = law.drop(index=[i])
    jack_r.append(dt["LSAT"].corr(dt["GPA"]))

jack_bias = (n - 1) * (np.mean(jack_r) - rhat)
print(jack_bias)

# bootstrap estimate of bias; boot() by hand
np.random.seed(5400)
law_LSAT = law["LSAT"].to_numpy()
def r(i):
    return np.corrcoef(law_LSAT[i], law_GPA[i])[0, 1]

boot_rep2 = np.array([r(np.random.randint(0, n, n)) for b in range(2000)])
boot_bias = np.mean(boot_rep2) - rhat
print(boot_bias)


## 5.2 Jackknife estimate of standard error

jack_se = ((n - 1) / n * np.sum((jack_r - np.mean(jack_r))**2))**0.5
print(jack_se)

# bootstrap estimate of se
boot_se = np.std(boot_rep2, ddof=1)
print(boot_se)


## 6.1 Method 1: standard normal bootstrap CI

from scipy.stats import bootstrap

np.random.seed(5400)
muhat = np.mean(law_GPA)
boot_se = bootstrap(data=(law_GPA,), statistic=np.mean,
  n_resamples=2000).standard_error
print(boot_se)
print(muhat + np.array([-1, 1]) * scipy.stats.norm.ppf(0.975) * boot_se)

# boot.ci(type = "norm") by hand: it also subtracts the bootstrap bias
def norm_ci(t0, t):
    bias = np.mean(t) - t0
    return t0 - bias + np.array([-1, 1]) * scipy.stats.norm.ppf(0.975) * np.std(t, ddof=1)

np.random.seed(5400)
n = len(law_GPA)
boot_t = np.mean(law_GPA[np.random.randint(0, n, size=(2000, n))], axis=1)
print(norm_ci(muhat, boot_t))


## 6.3 Method 2: basic bootstrap CI

# basic bootstrap CI
np.random.seed(5400)
n = len(law_GPA)
boot_t = np.mean(law_GPA[np.random.randint(0, n, size=(2000, n))], axis=1)
# method="weibull" is the same rule as R's quantile type = 6
boot_quan = np.quantile(boot_t, [0.975, 0.025], method="weibull")
print(2 * muhat - boot_quan)

np.random.seed(5400)
print(bootstrap(data=(law_GPA,), statistic=np.mean,
  n_resamples=2000, method='basic').confidence_interval)


## 6.4 Method 3: bootstrap percentile confidence interval

# bootstrap percentile CI
np.random.seed(5400)
n = len(law_GPA)
boot_t = np.mean(law_GPA[np.random.randint(0, n, size=(2000, n))], axis=1)
boot_quan = np.quantile(boot_t, [0.025, 0.975], method="weibull")
print(boot_quan)

np.random.seed(5400)
print(bootstrap(data=(law_GPA,), statistic=np.mean,
  n_resamples=2000, method='percentile').confidence_interval)


## 6.5 Method 4: bootstrap $t$ CI

# bootstrap t CI by hand: an inner bootstrap inside each outer one
np.random.seed(5400)
def mean_se(x, i):
    xi = x[i]
    idmat = np.random.randint(0, len(xi), size=(500, len(xi)))
    mu = np.mean(xi)
    v = np.var(np.mean(xi[idmat], axis=1), ddof=1)
    return mu, v

n = len(law_GPA)
t0, v0 = mean_se(law_GPA, np.arange(n))  # like boot.obj2$t0
t_star = np.empty(500)
for b in range(500):
    mu_b, v_b = mean_se(law_GPA, np.random.randint(0, n, n))
    t_star[b] = (mu_b - t0) / np.sqrt(v_b)
# boot.ci uses se = sqrt(v0); its quantile rule differs a little from np.quantile
print(t0 - np.quantile(t_star, [0.975, 0.025]) * np.sqrt(v0))


## 6.6 Method 5: BC$_a$

np.random.seed(5400)
print(bootstrap(data=(law_GPA,), statistic=np.mean,
  n_resamples=2000, method='bca').confidence_interval)


## 6.7 Comparing four intervals on a transformation

# Predict
# CIs for theta and exp(theta); norm_ci() is defined in Method 1
from scipy.stats import bootstrap

def mexp(x, axis=-1):
    return np.exp(np.mean(x, axis=axis))

n = len(law_GPA)
np.random.seed(5400)
boot_t = np.mean(law_GPA[np.random.randint(0, n, size=(2000, n))], axis=1)
allb = {"normal": norm_ci(np.mean(law_GPA), boot_t)}
allb_exp = {"normal": norm_ci(np.exp(np.mean(law_GPA)), np.exp(boot_t))}
for method in ["basic", "percentile", "bca"]:
    np.random.seed(5400)
    allb[method] = bootstrap((law_GPA,), np.mean, n_resamples=2000,
                             method=method).confidence_interval
    np.random.seed(5400)
    allb_exp[method] = bootstrap((law_GPA,), mexp, n_resamples=2000,
                                 method=method).confidence_interval

# Predict
for method in allb:
    print(f"{method:>10}", np.round(np.exp(allb[method]), 4),
          np.round(np.array(allb_exp[method]), 4))


## 6.8 Bootstrap confidence interval for the correlation

# population correlation
print(np.corrcoef(law82["LSAT"], law82["GPA"])[0, 1])

np.random.seed(5400)
print(bootstrap(data=(law_GPA, law_LSAT), statistic=my_corr,
  vectorized=False, paired=True, method='bca',
  n_resamples=2000).confidence_interval)

# basic and percentile intervals, for comparison with boot.ci
# a vectorized correlation: one value per resample, so it runs fast
def corr_vec(y, z, axis=-1):
    yc = y - y.mean(axis=axis, keepdims=True)
    zc = z - z.mean(axis=axis, keepdims=True)
    return (yc * zc).sum(axis) / np.sqrt((yc**2).sum(axis) * (zc**2).sum(axis))

for method in ["basic", "percentile"]:
    np.random.seed(5400)
    print(method, bootstrap(data=(law_GPA, law_LSAT), statistic=corr_vec,
      paired=True, method=method, n_resamples=2000).confidence_interval)


## 6.9 Application: a confidence interval for a model's accuracy

np.random.seed(5400)
n = 300
d = np.random.normal(size=n)                     # difficulty of each question
A = np.random.binomial(1, 1 / (1 + np.exp(-(1.0 + 2 * d))))   # 1 if model A is correct
B = np.random.binomial(1, 1 / (1 + np.exp(-(1.3 + 2 * d))))   # 1 if model B is correct
print(A.mean())
for method in ["percentile", "bca"]:
    np.random.seed(5400)
    print(method, bootstrap((A,), np.mean, n_resamples=2000, method=method).confidence_interval)
print(scipy.stats.binomtest(int(A.sum()), n).proportion_ci(method="wilson"))   # Wilson interval

# Predict
np.random.seed(5400)
idmat = np.random.randint(0, n, size=(2000, n))            # resampled questions
boot_D = np.array([np.mean(B[i] - A[i]) for i in idmat])   # question i keeps its pair
print(np.mean(B - A))
print(np.std(boot_D, ddof=1))                              # paired bootstrap SE
print(np.quantile(boot_D, [0.025, 0.975], method="weibull"))

# Predict
# wrong: resample A and B separately, which breaks the pairs
wrong = [np.mean(np.random.choice(B, n)) - np.mean(np.random.choice(A, n)) for b in range(2000)]
print(np.std(wrong, ddof=1))

np.random.seed(5400)
G, m = 60, 5
pg = np.random.choice([0.9, 0.5], G)                       # a passage is easy or hard
Ymat = np.random.binomial(1, np.repeat(pg, m)).reshape(G, m)   # one row per passage
print(Ymat.mean())
se_q = np.std([np.mean(np.random.choice(Ymat.ravel(), G * m)) for b in range(2000)], ddof=1)
se_g = np.std([Ymat[np.random.randint(0, G, G)].mean() for b in range(2000)], ddof=1)
print(se_q, se_g, se_g / se_q)


## 7.1 {{< fa user-graduate >}} Fisher transformation

def FisherTrans(theta):
    return 0.5 * np.log((1 + theta) / (1 - theta))

print(np.std(FisherTrans(np.array(boot_par_cor)), ddof=1))
print(1 / np.sqrt(law.shape[0] - 3))

import matplotlib.pyplot as plt
import scipy.stats

zeta = FisherTrans(np.array(boot_par_cor))
fig, ax = plt.subplots(1, 2)
ax[0].hist(zeta, edgecolor='k')
ax[0].set_title("Histogram of zeta")
# normal QQ plot with its reference line (qqnorm plus qqline)
scipy.stats.probplot(zeta, dist="norm", plot=ax[1])
plt.show()


## 7.2 {{< fa user-graduate >}} An improved bias estimate

law_LSAT = law["LSAT"].to_numpy()
n = len(law_GPA)

def bootBias(B):
    rhat = np.corrcoef(law_LSAT, law_GPA)[0, 1]
    idmat = np.random.randint(0, n, size=(B, n))  # random index
    Y, Z = law_LSAT[idmat], law_GPA[idmat]         # B x n matrices
    rhat_star = np.corrcoef(Y.ravel(), Z.ravel())[0, 1]
    # correlation of each row, all B rows at once
    Yc = Y - Y.mean(axis=1, keepdims=True)
    Zc = Z - Z.mean(axis=1, keepdims=True)
    boot_r = (Yc * Zc).sum(axis=1) / np.sqrt((Yc**2).sum(axis=1) * (Zc**2).sum(axis=1))
    bias1 = np.mean(boot_r - rhat)       # bootstrap estimate of bias
    bias2 = np.mean(boot_r - rhat_star)  # improved estimate
    return bias1, bias2                  # return

import matplotlib.pyplot as plt

np.random.seed(5400)
Blist = [25, 50, 100, 200, 400, 800, 1000, 1300, 1600, 2000, 2500, 3200]
bias = np.array([bootBias(B) for B in Blist])

plt.plot(Blist, bias[:, 0], "k-", label="bootstrap est of bias")
plt.plot(Blist, bias[:, 1], "k--", label="improved bootstrap of bias")
plt.axhline(bootBias(10000)[0], linestyle=":", color="blue",
            label="ideal bootstrap estimate")
plt.xticks(Blist, rotation=90)
plt.xlabel("B")
plt.ylabel("bias")
plt.legend(loc="upper right")
plt.show()


## 7.3 {{< fa user-graduate >}} Failure of the jackknife: the median

# Predict
np.random.seed(5400)
law_LSAT = law["LSAT"].to_numpy()
n = len(law_LSAT)
# np.delete(x, i) drops element i, like x[-i] in R
jack_r = np.array([np.median(np.delete(law_LSAT, i)) for i in range(n)])
print(jack_r)

# Predict
jack_se = np.sqrt((n - 1) / n * np.sum((jack_r - np.mean(jack_r))**2))
print(jack_se)

# Predict
# boot() by hand: 2000 index vectors, one per row
np.random.seed(5400)
idmat = np.random.randint(0, n, size=(2000, n))
boot_rep = np.median(law_LSAT[idmat], axis=1)
boot_se = np.std(boot_rep, ddof=1)
print(boot_se)


## 7.5 {{< fa user-graduate >}} Jackknife-after-bootstrap

np.random.seed(5400)
# jackknife after bootstrap
law_LSAT = law["LSAT"].to_numpy()
B = 400; n = len(law_GPA)
# save indices
indices = np.random.randint(0, n, size=(B, n))
boot_r = np.array([np.corrcoef(law_LSAT[idx], law_GPA[idx])[0, 1]
                   for idx in indices])

jack_boot_se = np.empty(n)
for i in range(n):
    keep = ~(indices == i).any(axis=1)  # samples that leave out point i
    jack_boot_se[i] = np.std(boot_r[keep], ddof=1)

# bootstrap estimate of se
print(np.std(boot_r, ddof=1))
# jackknife-after-bootstrap estimate of its own variability
print(np.sqrt((n - 1) * np.mean((jack_boot_se - np.mean(jack_boot_se))**2)))


## 7.6 {{< fa user-graduate >}} Resampling big data: half-sampling and the Poisson bootstrap

np.random.seed(5400)
x = law_GPA; n = len(x)
print(np.std(x, ddof=1) / np.sqrt(n))                                           # formula
print(np.std([np.mean(np.random.choice(x, n)) for b in range(2000)], ddof=1))   # ordinary bootstrap
print(np.std([np.mean(np.random.choice(x, n // 2, replace=False)) for b in range(2000)], ddof=1))   # half-sampling
w = np.random.poisson(1, size=(2000, n))                                        # one count per observation
print(np.std((w * x).sum(axis=1) / w.sum(axis=1), ddof=1))                      # Poisson bootstrap
