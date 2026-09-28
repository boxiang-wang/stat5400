# STAT:5400 Section 1.1 — Introduction
# Code from the lecture notes; no output, no solutions.

if (dir.exists("~/classdata/models/R")) .libPaths(c("~/classdata/models/R", .libPaths()))  # on IDAS: the class copy of ellmer
# Start the Ollama server if it is not running yet (needed once per IDAS session)
ollama_up <- function() !inherits(try(suppressWarnings(readLines("http://localhost:11434/api/version")), silent = TRUE), "try-error")
if (!ollama_up()) {
  if (dir.exists("~/classdata/models")) {             # on IDAS: use the class copy of Ollama and its models
    Sys.setenv(PATH = paste0(path.expand("~/classdata/models/ollama/bin:"), Sys.getenv("PATH")),
               OLLAMA_MODELS = path.expand("~/classdata/models/library"), OLLAMA_NOPRUNE = "1")
  }
  if (nzchar(Sys.which("ollama"))) {                  # skip if Ollama is not installed
    system("nohup ollama serve > ~/ollama.log 2>&1 &")  # start it in the background
    for (i in 1:30) if (ollama_up()) break else Sys.sleep(1)
  }
}


## 7 Set up your accounts

# Run
set.seed(5400)
x <- rnorm(100)
mean(x)

library(ellmer)
small  <- chat_ollama(model = "qwen2.5:0.5b")
bigger <- chat_ollama(model = "llama3.2:1b")
small$chat("Which is larger, 9.11 or 9.9? Answer in one line.")
bigger$chat("Which is larger, 9.11 or 9.9? Answer in one line.")


## 9 Optimization

# Run
temp   <- c(53, 57, 58, 63, 66, 67, 67, 67, 68, 69, 70, 70, 70, 70, 72, 73, 75, 75, 76, 76, 78, 79, 81)
damage <- c( 5,  1,  1,  1,  0,  0,  0,  0,  0,  0,  1,  0,  1,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0)
fit <- glm(cbind(damage, 6 - damage) ~ temp, family = binomial)
coef(fit)
predict(fit, data.frame(temp = c(31, 53, 70)), type = "response")   # P(an O-ring fails)


## 10 Demonstration of better implementation

set.seed(5400)
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
set.seed(5400)
x <- runif(1e6)
timeit(
  sqrt(x),
  x ^ 0.5
)

# Edit
set.seed(5400)
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

set.seed(5400)
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
set.seed(5400)
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
