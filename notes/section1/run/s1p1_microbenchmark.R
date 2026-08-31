# STAT 5400 - Section 1.1 - Demonstration of better implementation
library(microbenchmark)

x <- runif(100)
microbenchmark(
  sqrt(x),
  x ^ 0.5
)

x <- runif(1000)
microbenchmark(
  x * x * x,
  x ^ 3,
  x * 0.1,
  x / 10
)

x <- matrix(2, 100, 100)
microbenchmark(
  colMeans(x),
  rowMeans(x)
)
