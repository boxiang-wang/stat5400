# Section 3.2 -- six confidence intervals for a binomial proportion, at the
# full B = 10000 of the slides. Too slow for the browser; run it here.
library(binom)

set.seed(5400)
theta <- 0.6
n <- 40
B <- 10000
alp <- 0.05
Xbarlist <- rbinom(B, size = n, prob = theta) / n

## Wald interval
moe_Wald <- qnorm(1 - alp/2) * sqrt(Xbarlist * (1 - Xbarlist)/n)
CI_Wald <- cbind(Xbarlist - moe_Wald, Xbarlist + moe_Wald)

## simple conservative interval
moe_simple <- qnorm(1 - alp/2) * sqrt(0.5 * (1 - 0.5)/n)
CI_simple <- cbind(Xbarlist - moe_simple, Xbarlist + moe_simple)

## score, CP, AC, and the Jeffreys Bayesian CIs
CI_score <- CI_CP <- CI_AC <- CI_Bayes <- matrix(NA, B, 2)
for (i in seq(B)) {
  CI_score[i, ] <- prop.test(x = (n * Xbarlist[i]), n = n,
    correct = FALSE, conf.level = (1 - alp))$conf.int
  CI_CP[i, ] <- binom.test(x = (n * Xbarlist[i]), n = n,
    conf.level = (1 - alp))$conf.int
  ret <- binom.confint(x = (n * Xbarlist[i]), n = n,
    conf.level = (1 - alp), methods = "ac")
  CI_AC[i, ] <- c(ret$lower, ret$upper)
  ret2 <- binom.bayes(x = (n * Xbarlist[i]), n = n,
    type = "central", conf.level = (1 - alp))
  CI_Bayes[i, ] <- c(ret2$lower, ret2$upper)
}

WidthCov <- function(CI) {
  is_cov <- function(x) theta > x[1] & theta < x[2]
  se <- function(x) sd(x) / sqrt(nrow(CI))
  allwidth <- CI[, 2] - CI[, 1]
  allcov <- apply(CI, 1, is_cov)
  c(mean(allwidth), se(allwidth), mean(allcov), se(allcov))
}

col.nm <- paste0("CI_", c("simple", "Wald", "score", "CP", "AC", "Bayes"))
res <- sapply(lapply(col.nm, get), WidthCov)
colnames(res) <- col.nm
rownames(res) <- c("exp.width", "se", "cov.prob", "se")
round(res, 3)
