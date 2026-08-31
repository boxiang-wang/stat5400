# STAT 5400 - Section 1.1 - R loop vs C++ (Rcpp) vs built-in sum()
# Source: Advanced R
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

x <- runif(1e3)
microbenchmark(sum(x), sumC(x), sumR(x))
