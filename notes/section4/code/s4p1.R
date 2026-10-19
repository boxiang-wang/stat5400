# STAT:5400 Section 4.1 — Bootstrap and Jackknife
# Code from the lecture notes; no output, no solutions.

## 1.3 Datasets `law82` and `law`

law <- read.csv("data/law.csv")
law82 <- read.csv("data/law82.csv")
head(law82)

sampled.school <- merge(law82, law, by = c("LSAT", "GPA"))$School
head(within(law82, sampled <- School %in% sampled.school))


## 1.4 Confidence interval for the population mean

(n <- length(law$GPA))
mean(law$GPA)

(se <- sd(law$GPA) / sqrt(n))
mean(law$GPA) + 2 * c(-1, 1) * se

# check the true population mean
mean(law82$GPA)


## 1.6 Confidence interval for the population median

median(law$GPA)
(se <- sd(law$GPA) / sqrt(n) * sqrt(pi/2))

median(law$GPA) + 2 * c(-1, 1) * se
# check the true population median
median(law82$GPA)


## 1.8 One bootstrap sample

# Predict
set.seed(5400)
x <- c(0.3, 0.7, 1.2, 1.4, 2.1)              # original sample
median(x)                                    # s(X)
(boot.samp <- sample(x, replace = TRUE))     # one bootstrap sample X*
median(boot.samp)                            # s(X*)


## 1.11 A toy example

set.seed(5400)
# original sample
x <- c(0.3, 0.7, 1.2, 1.4, 2.1)
median(x)

# Generate B bootstrap samples and replications
boot.rep <- rep(NA, 200)
for (b in seq(200)) {
  boot.sample <- sample(x, replace = TRUE)
  boot.rep[b] <- median(boot.sample)
}
sd(boot.rep)

set.seed(5400)
# one bootstrap sample per column
boot.samp <- replicate(200, sample(x, replace = TRUE))
boot.rep <- apply(boot.samp, 2, median)
sd(boot.rep)
hist(boot.rep, main = "Histogram of Bootstrap Replications")


## 1.12 Example: `law82` and `law`

set.seed(5400)
B <- 200
boot.samp <- replicate(B, sample(law$GPA, replace = TRUE))
boot.rep <- apply(boot.samp, 2, median)
sd(boot.rep)

hist(boot.rep, main = "Histogram of Bootstrap Replications")


## 1.13 R package `boot`

library(boot)
set.seed(5400)
m <- function(x, i) median(x[i])
boot.rep2 <- boot(data = law$GPA, statistic = m, R = 200)
sd(boot.rep2$t)


## 1.15 True standard error of the sample median

set.seed(5400)
B <- 200
real.samp <- replicate(B, sample(law82$GPA, 15, replace = TRUE))
samp.dist.median <- apply(real.samp, 2, median)
sd(samp.dist.median)


## 2.4 Example 2 of empirical distribution

law$GPA

mean(law$GPA < 3)


## 2.8 Example: correlation coefficient

cor(law$LSAT, law$GPA) # the sample correlation

# use bootstrap to estimate the standard error
set.seed(5400)
B <- 200; n <- nrow(law)
boot.rep <- rep(NA, B)
for (b in seq(B)) {
  id <- sample(n, n, replace = TRUE)
  boot.rep[b] <- cor(law$LSAT[id], law$GPA[id])
}
sd(boot.rep)

set.seed(5400)
r <- function(x, i) cor(x[i, 1], x[i, 2])
boot.rep2 <- boot(data = law, statistic = r, R = 200)
sd(boot.rep2$t)


## 2.9 Population sampling versus bootstrap sampling

set.seed(5400)
n <- nrow(law)
sample.cor <- rep(NA, 200)
for (b in seq(200)) {
  id <- sample(82, n, replace = TRUE)
  sample.cor[b] <- cor(law82$LSAT[id], law82$GPA[id])
}

set.seed(5400)
par(mfrow = c(1, 2))
hist(sample.cor,
  xlab = "Random Samples from Population",
  main = "", breaks = seq(-0.1, 1, 0.1))
hist(boot(data = law, statistic = r, R = 200)$t,
  breaks = seq(-0.1, 1, 0.1),
  xlab = "Bootstrap", main = "")


## 3.1 Nonparametric and parametric bootstrap

library(MASS)
set.seed(5400)
# mean and cov for generating bivariate normal var
mu <- colMeans(law)
covmat <- cov(law)

# parametric bootstrap replications of the correlation
boot.par.cor <- rep(NA, 200)
for (b in seq(200)) {
  boot.par.cor[b] <- cor(mvrnorm(n = 15, mu, covmat))[2]
}
sd(boot.par.cor)

set.seed(5400)
par(mfrow = c(1, 2))
hist(boot(data = law, statistic = r, R = 200)$t,
  breaks = seq(0, 1, 0.1),
  xlab = "Nonparametric Bootstrap", main = "")
hist(boot.par.cor, breaks = seq(0, 1, 0.1),
  xlab = "Parametric Bootstrap", main = "")


## 3.2 Standard error of the sample correlation coefficient

(rhat <- cor(law$LSAT, law$GPA))
(1 - rhat^2) / sqrt(nrow(law) - 3)


## 4.2 Bootstrap estimation of bias

set.seed(5400)
# sample estimate of correlation
(rhat <- cor(law$LSAT, law$GPA))

# bootstrap estimate of bias
B <- 200; n <- nrow(law)
boot.r <- rep(NA, B)
for (b in seq(B)) {
  id <- sample(n, n, replace = TRUE)
  boot.r[b] <- cor(law$LSAT[id], law$GPA[id])
}
(bias <- mean(boot.r - rhat))

bias / sd(boot.r)
2 * sd(boot.r) / sqrt(200)


## 4.5 Application: the bias of the best of 20 prompts

# Predict
set.seed(5400)
K <- 20; n <- 200
Y <- matrix(rbinom(K * n, 1, 0.70), K, n)      # row k: prompt k on the 200 questions
(theta.hat <- max(rowMeans(Y)))                # accuracy of the best prompt
best <- function(d, i) max(colMeans(d[i, ]))   # d has one row per question
boot.obj <- boot(data = t(Y), statistic = best, R = 2000)
(bias <- mean(boot.obj$t) - theta.hat)         # bootstrap estimate of bias
bias / sd(boot.obj$t)


## 5.1 Jackknife estimate of bias

set.seed(5400)
(rhat <- cor(law$LSAT, law$GPA))
n <- nrow(law)
# jackknife estimate of bias
jack.r <- rep(NA, n)
for (i in seq(n)) {
  jack.r[i] <- cor(law$LSAT[-i], law$GPA[-i])
}
(jack.bias <- (n - 1) * (mean(jack.r) - rhat))

# bootstrap estimate of bias
set.seed(5400)
r <- function(x, i) cor(x[i, 1], x[i, 2])
boot.rep2 <- boot(data = law, statistic = r, R = 2000)
(boot.bias <- mean(boot.rep2$t) - rhat)


## 5.2 Jackknife estimate of standard error

# jackknife estimate of se
(jack.se <- sqrt((n - 1) / n * sum((jack.r - mean(jack.r))^2)))

# bootstrap estimate of se
(boot.se <- sd(boot.rep2$t))


## 6.1 Method 1: standard normal bootstrap CI

set.seed(5400)
# sample mean
muhat <- mean(law$GPA)
m <- function(x, i) mean(x[i])
# bootstrap estimate of se
boot.obj <- boot(data = law$GPA, statistic = m, R = 2000)
(boot.se <- sd(boot.obj$t))

muhat + c(-1, 1) * qnorm(0.975) * boot.se

# from boot package
boot.ci(boot.obj, type = "norm")


## 6.3 Method 2: basic bootstrap CI

# basic bootstrap CI
set.seed(5400)
boot.obj <- boot(data = law$GPA, statistic = m, R = 2000)
boot.quan <- quantile(boot.obj$t, c(0.975, 0.025), type = 6)
2 * muhat - boot.quan

# from boot package
boot.ci(boot.obj, type = "basic")


## 6.4 Method 3: bootstrap percentile confidence interval

# bootstrap percentile CI
set.seed(5400)
boot.obj <- boot(data = law$GPA, statistic = m, R = 2000)
(boot.quan <- quantile(boot.obj$t, c(0.025, 0.975), type = 6))

# from boot package
boot.ci(boot.obj, type = "perc")


## 6.5 Method 4: bootstrap $t$ CI

# use bootstrap to estimate se
set.seed(5400)
mean.se <- function(x, i) {
  m <- function(x, i) mean(x[i])
  mu <- mean(x[i])
  v <- var(boot(data = x[i], statistic = m, R = 500)$t)
  c(mu, v)
}
boot.obj2 <- boot(data = law$GPA, statistic = mean.se, R = 500)
boot.ci(boot.obj2, type = "stud")


## 6.6 Method 5: BC$_a$

# BCa
set.seed(5400)
boot.obj <- boot(data = law$GPA, statistic = m, R = 2000)
boot.ci(boot.obj, type = "bca")


## 6.7 Comparing four intervals on a transformation

# Predict
# CIs for theta and exp(theta)
m <- function(x, i) mean(x[i])
mexp <- function(x, i) exp(mean(x[i]))
set.seed(5400)
boot.obj <- boot(data = law$GPA, statistic = m, R = 2000)
set.seed(5400)
boot.exp <- boot(data = law$GPA, statistic = mexp, R = 2000)
allb <- unlist(boot.ci(boot.obj, type = c("norm", "basic", "perc", "bca")))
allb.exp <- unlist(boot.ci(boot.exp, type = c("norm", "basic", "perc", "bca")))

# Predict
rbind(
  normal   = c(exp(c(allb$normal2, allb$normal3)),
               c(allb.exp$normal2, allb.exp$normal3)),
  basic    = c(exp(c(allb$basic4, allb$basic5)),
               c(allb.exp$basic4, allb.exp$basic5)),
  percent  = c(exp(c(allb$percent4, allb$percent5)),
               c(allb.exp$percent4, allb.exp$percent5)),
  bca      = c(exp(c(allb$bca4, allb$bca5)),
               c(allb.exp$bca4, allb.exp$bca5)))


## 6.8 Bootstrap confidence interval for the correlation

set.seed(5400)
# population correlation
cor(law82$LSAT, law82$GPA)

# estimate cor and the variance of the bootstrap replicates
set.seed(5400)
mean.se <- function(x, i) {
  corfun <- function(x, i) cor(x$LSAT[i], x$GPA[i])
  v <- var(boot(data = x[i, ], statistic = corfun, R = 500)$t)
  c(corfun(x, i), v)
}
boot.obj <- boot(data = law, statistic = mean.se, R = 500)   # try at home: R = 2000 in both loops
boot.ci(boot.obj, type = "all")


## 6.9 Application: a confidence interval for a model's accuracy

set.seed(5400)
n <- 300
d <- rnorm(n)                                    # difficulty of each question
A <- rbinom(n, 1, plogis(1.0 + 2 * d))           # 1 if model A is correct
B <- rbinom(n, 1, plogis(1.3 + 2 * d))           # 1 if model B is correct
mean(A)
acc <- function(x, i) mean(x[i])
boot.A <- boot(A, acc, R = 2000)
boot.ci(boot.A, type = c("perc", "bca"))
prop.test(sum(A), n, correct = FALSE)$conf.int   # Wilson interval, Section 3.2

# Predict
set.seed(5400)
dat <- data.frame(A, B)
dif <- function(x, i) mean(x$B[i] - x$A[i])     # question i keeps its pair (A_i, B_i)
boot.D <- boot(dat, dif, R = 2000)
mean(B - A)
sd(boot.D$t)                                    # paired bootstrap SE
boot.ci(boot.D, type = "perc")

# Predict
# wrong: resample A and B separately, which breaks the pairs
set.seed(5400)
wrong <- replicate(2000, mean(sample(B, replace = TRUE)) - mean(sample(A, replace = TRUE)))
sd(wrong)

set.seed(5400)
G <- 60; m <- 5
pg <- sample(c(0.9, 0.5), G, replace = TRUE)               # a passage is easy or hard
Ymat <- matrix(rbinom(G * m, 1, rep(pg, each = m)), G, m, byrow = TRUE)   # one row per passage
mean(Ymat)
se.q <- sd(replicate(2000, mean(sample(Ymat, replace = TRUE))))         # resample questions
se.g <- sd(replicate(2000, mean(Ymat[sample(G, replace = TRUE), ])))    # resample passages
c(questions = se.q, passages = se.g, ratio = se.g / se.q)


## 7.1 {{< fa user-graduate >}} Fisher transformation

FisherTrans <- function(theta) {
  0.5 * log((1 + theta) / (1 - theta))
}
sd(FisherTrans(boot.par.cor))
1 / sqrt(nrow(law) - 3)

zeta <- FisherTrans(boot.par.cor)
par(mfrow = c(1, 2))
hist(zeta)
qqnorm(zeta)
qqline(zeta)


## 7.2 {{< fa user-graduate >}} An improved bias estimate

bootBias <- function(B) {
  n <- nrow(law)
  rhat <- cor(law$LSAT, law$GPA)
  idmat <- matrix(sample(n, n * B, replace = TRUE), B, n) # random index
  rhat.star <- cor(law$LSAT[idmat], law$GPA[idmat])
  boot.r <- apply(idmat, 1, function(x) cor(law$LSAT[x], law$GPA[x]))
  bias1 <- mean(boot.r - rhat)       # bootstrap estimate of bias
  bias2 <- mean(boot.r - rhat.star)  # improved estimate
  c(bias1, bias2)                    # return
}

set.seed(5400)
Blist <- c(25, 50, 100, 200, 400, 800, 1000, 1300, 1600, 2000, 2500, 3200)
bias <- t(sapply(Blist, bootBias))

plot(Blist, bias[, 1], type = "l", lty = 1,
  ylim = range(bias), xaxt = "n", ylab = "bias", xlab = "B")
axis(1, at = Blist)
points(Blist, bias[, 2], type = "l", lty = 2)
abline(h = bootBias(10000)[1], lty = 3, col = "blue")
legend("topright", c("bootstrap est of bias",
  "improved bootstrap of bias", "ideal bootstrap estimate"),
  lty = 1:3, col = c(1, 1, 4))


## 7.3 {{< fa user-graduate >}} Failure of the jackknife: the median

# Predict
set.seed(5400)
n <- nrow(law)
jack.r <- sapply(1:n, function(x) median(law$LSAT[-x]))
jack.r

# Predict
(jack.se <- sqrt((n - 1) / n * sum((jack.r - mean(jack.r))^2)))

# Predict
set.seed(5400)
m <- function(x, i) median(x[i])
boot.rep <- boot(data = law$LSAT, statistic = m, R = 2000)
(boot.se <- sd(boot.rep$t))


## 7.5 {{< fa user-graduate >}} Jackknife-after-bootstrap

set.seed(5400)
# jackknife after bootstrap
B <- 400; n <- nrow(law)
# save indices
indices <- matrix(NA, B, n)
boot.r <- rep(NA, B)
for (b in seq(B)) {
  id <- sample(n, n, replace = TRUE)
  boot.r[b] <- cor(law$LSAT[id], law$GPA[id])
  indices[b, ] <- id
}

jack.boot.se <- rep(NA, n)
for (i in seq(n)) {
  keep <- seq(B)[apply(indices, 1, function(x) !(i %in% x))]
  jack.boot.se[i] <- sd(boot.r[keep])
}

# bootstrap estimate of se
sd(boot.r)
# jackknife-after-bootstrap estimate of its own variability
sqrt((n - 1) * mean((jack.boot.se - mean(jack.boot.se))^2))


## 7.6 {{< fa user-graduate >}} Resampling big data: half-sampling and the Poisson bootstrap

set.seed(5400)
x <- law$GPA; n <- length(x)
sd(x) / sqrt(n)                                                  # formula
sd(replicate(2000, mean(sample(x, replace = TRUE))))             # ordinary bootstrap
sd(replicate(2000, mean(sample(x, n %/% 2))))                    # half-sampling
sd(replicate(2000, { w <- rpois(n, 1); sum(w * x) / sum(w) }))   # Poisson bootstrap
