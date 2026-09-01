# STAT:5400 Section 1.1 — Introduction
# Code from the lecture notes; no output, no solutions.

## 7 Set up your accounts

# Run
x <- rnorm(100)
mean(x)


## 9 Optimization

# Run
temp   <- c(53, 57, 58, 63, 66, 67, 67, 67, 68, 69, 70, 70, 70, 70, 72, 73, 75, 75, 76, 76, 78, 79, 81)
damage <- c( 5,  1,  1,  1,  0,  0,  0,  0,  0,  0,  1,  0,  1,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0)
fit <- glm(cbind(damage, 6 - damage) ~ temp, family = binomial)
coef(fit)
predict(fit, data.frame(temp = c(31, 53, 70)), type = "response")   # P(an O-ring fails)


## 10 Demonstration of better implementation

library(microbenchmark)

x <- runif(100)
microbenchmark(
  sqrt(x),
  x ^ 0.5
)

timeit <- function(..., times = 10) {
  exprs <- as.list(substitute(list(...)))[-1]
  env <- parent.frame()
  out <- t(sapply(exprs, function(e) {
    el <- replicate(times, system.time(eval(e, env))[["elapsed"]])
    c(median_ms = 1000 * median(el), min_ms = 1000 * min(el))
  }))
  rownames(out) <- sapply(exprs, function(e) paste(deparse(e), collapse = ""))
  round(out, 2)
}

# Run
x <- runif(1e6)
timeit(
  sqrt(x),
  x ^ 0.5
)

# Edit
x <- runif(1e6)
timeit(
  x * x * x,
  x ^ 3,
  x * 0.1,
  x / 10
)

x <- matrix(2, 1000, 1000)
timeit(
  colMeans(x),
  rowMeans(x)
)

# Run
A1 <- matrix(2, 1000, 1000)
A2 <- matrix(2, 1000, 1000)
A3 <- rep(2, 1000)

system.time(A1 %*% A2 %*% A3)
system.time(A1 %*% (A2 %*% A3))

library(Rcpp)
library(microbenchmark)
sumR <- function(x) {
  total <- 0
  for (i in seq_along(x)) 
    total <- total + x[i]
  total
}
cppFunction('double sumC(NumericVector x){
  int n = x.size();
  double total = 0;
  for (int i=0; i < n; i++) {
    total += x[i];
  }
  return total;
}')
x = runif(1e3)
microbenchmark(sum(x), sumC(x), sumR(x))

# By hand
sumR <- function(x) {
  # your code here

}

x <- runif(1e5)
all.equal(sumR(x), sum(x))
timeit(sum(x), sumR(x))

# Vibe
bench_pow <- function(n) {
  # return: median time of x^0.5
  #         / median time of sqrt(x)

}
# n_grid <- 10^(4:6); ratios <- sapply(n_grid, bench_pow)
# plot(n_grid, ratios, log = "x", type = "b")


## 17.1 Your first API call

library(ellmer)
models_google_gemini()                # which models your key can use; pick a "flash" one
chat <- chat_google_gemini(model = "gemini-3.7-flash")   # reads GEMINI_API_KEY from the environment
chat$chat("In one sentence, what does a statistician do that a chatbot cannot?")
