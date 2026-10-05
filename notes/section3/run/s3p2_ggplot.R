# Section 3.2 -- one-dimensional sample means at four sample sizes.
# ggplot2 is not installed in the browser session.
library(ggplot2)

set.seed(5400)
n <- rep(c(10, 25, 40, 100), each = 100)
y <- sapply(n, function(n) mean(rnorm(n)))

ggplot() + geom_point(aes(y, factor(n)),
  position = position_jitter(height = 0.15)) +
  labs(x = "sample mean", y = "sample size")
