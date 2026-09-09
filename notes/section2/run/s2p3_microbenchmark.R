# Section 2.3 -- timing three factorial implementations.
# microbenchmark needs a precise clock, so it cannot run in the browser.
library(microbenchmark)

MyFactorial1 <- function(nseq) {
  return(sapply(nseq, factorial))
}

MyFactorial2 <- function(nseq) {
  return(sapply(nseq,
    function(x) Reduce('*', seq(x))))
}

microbenchmark(
  factorial(c(5, 8, 10)),
  MyFactorial1(c(5, 8, 10)),
  MyFactorial2(c(5, 8, 10))
)
