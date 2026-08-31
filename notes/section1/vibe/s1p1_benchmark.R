# STAT 5400 - Section 1.1 - Vibe task
# Open this file in a Codespace (Copilot on) and let the completion help you.
#
# TASK: write a function  bench_pow(n)  that
#   1. draws x <- runif(n),
#   2. times  sqrt(x)  and  x^0.5  (use microbenchmark on your machine, or system.time),
#   3. returns the ratio of their median times (x^0.5 over sqrt),
# then call it for n = 10^(2:6) and plot the ratio against n (log-x axis).
# Verify: the ratio should be well above 1 for large n.

library(microbenchmark)

bench_pow <- function(n) {

}
