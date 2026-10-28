# STAT:5400 Tech Guide 3 — R Packages
# Code from the lecture notes; no output, no solutions.

## 1.1 From CRAN

install.packages("profvis")
library(profvis)
packageVersion("profvis")

.libPaths()


## 1.2 On the lnx machines

Sys.getenv("R_LIBS_USER")                   # the personal library
dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE, showWarnings = FALSE)


## 1.3 From GitHub

install.packages("remotes")
remotes::install_github("rladies/praise")
praise::praise()


## 1.5 Build tools

if (!requireNamespace("devtools", quietly = TRUE)) install.packages("devtools")
devtools::has_devel()


## 2.1 The package `devtools`

library(devtools)


## 2.3 Creating an R package

mydir <- "~/STAT5400/package"
dir.create(mydir, recursive = TRUE, showWarnings = FALSE)
setwd(mydir)

if (dir.exists("pvalDist")) unlink("pvalDist", recursive = TRUE)
create_package("pvalDist", open = FALSE)
list.files("pvalDist", all.files = TRUE, no.. = TRUE)

cat(file = "pvalDist/DESCRIPTION", r"---(Package: pvalDist
Type: Package
Title: Simulated P-Values of the One-Sample t Test
Version: 0.0.1
Date: 2026-10-28
Authors@R: c(person(given = "Boxiang", family = "Wang",
                    role = c("aut", "cre"), email = "boxiang-wang@uiowa.edu"),
             person(given = "Indiana", family = "Jones", role = "aut"))
Description: Simulates the p-values of the one-sample t test when the data
    come from a user-specified distribution. The package is used in
    STAT:5400 to show how to create an R package.
License: GPL-3
Encoding: UTF-8
Imports: stats
Roxygen: list(markdown = TRUE)
)---")

cat(file = "pvalDist/R/pvalDist2.R", r"---(#' Simulated p-values of the one-sample t test
#'
#' Simulates `B` samples of size `n` from a distribution and returns the
#' `B` p-values of the two-sided one-sample t test of `mu_0`.
#'
#' @param n Sample size.
#' @param dist Name of the distribution without the leading `r`, for
#'   example `"norm"` or `"exp"`.
#' @param mu_0 The population mean under the null hypothesis.
#' @param B Number of simulated samples.
#' @param ... Further arguments passed to the random number generator,
#'   for example `rate = 1/2`.
#' @return A vector of `B` p-values.
#' @examples
#' set.seed(5400)
#' p <- pvalDist2(n = 10, dist = "exp", mu_0 = 2, B = 1000, rate = 1/2)
#' mean(p < 0.05)   # Type I error
#' @importFrom stats pt sd
#' @export
pvalDist2 <- function(n, dist, mu_0, B = 10000, ...) {
  # simulate data from user-specified dist
  Xlist <- do.call(paste0("r", dist), list(B * n, ...))
  Xlist <- matrix(Xlist, B, n)
  # compute t-statistic for each sample
  Xbarlist <- rowMeans(Xlist)
  sdlist <- apply(Xlist, 1, sd)
  t_stat <- (Xbarlist - mu_0) / (sdlist / sqrt(n))
  # returns the observed p-values
  pt(-abs(t_stat), n - 1) + 1 - pt(abs(t_stat), n - 1)
}
)---")

document("pvalDist")
cat(readLines("pvalDist/NAMESPACE"), sep = "\n")

rmarkdown::pandoc_available()
proj_set("pvalDist")
use_vignette("pvalDist")
build_vignettes("pvalDist")

system("R CMD build pvalDist")
system("R CMD INSTALL pvalDist_0.0.1.tar.gz")

system("R CMD check pvalDist_0.0.1.tar.gz")

library(pvalDist)
packageVersion("pvalDist")
set.seed(5400)
p <- pvalDist2(n = 10, dist = "exp", mu_0 = 2, B = 1000, rate = 1/2)
mean(p < 0.05)


## 3 Extending R with C++ and Fortran

tstat_R <- function(x, mu_0) {
  n <- length(x)
  (mean(x) - mu_0) / (sd(x) / sqrt(n))
}


## 3.1 C++

cat(file = "tstat_C.cpp", r"---(#include <Rcpp.h>
using namespace Rcpp;

//' One-sample t statistic (C++)
//'
//' @param x A numeric vector.
//' @param mu_0 The population mean under the null hypothesis.
//' @return The t statistic.
//' @examples
//' tstat_C(c(1, 2, 3, 5), mu_0 = 2)
//' @export
// [[Rcpp::export]]
double tstat_C(NumericVector x, double mu_0) {
  int n = x.size();
  double s = 0.0, ss = 0.0;
  for (int i = 0; i < n; i++) s += x[i];
  double xbar = s / n;
  for (int i = 0; i < n; i++) ss += (x[i] - xbar) * (x[i] - xbar);
  double sd = sqrt(ss / (n - 1));
  return (xbar - mu_0) / (sd / sqrt(n));
}
)---")

if (!requireNamespace("Rcpp", quietly = TRUE)) install.packages("Rcpp")
Rcpp::sourceCpp("tstat_C.cpp")
x <- c(1, 2, 3, 5)
tstat_R(x, mu_0 = 2)
tstat_C(x, mu_0 = 2)


## 3.2 Fortran

cat(file = "tstat_f.f90", r"---(subroutine tstat_f(n, x, mu0, t)
  implicit none
  integer, intent(in) :: n
  double precision, intent(in) :: x(n), mu0
  double precision, intent(out) :: t
  integer :: i
  double precision :: xbar, ss
  xbar = 0.0d0
  do i = 1, n
    xbar = xbar + x(i)
  end do
  xbar = xbar / dble(n)
  ss = 0.0d0
  do i = 1, n
    ss = ss + (x(i) - xbar)**2
  end do
  t = (xbar - mu0) / (sqrt(ss / dble(n - 1)) / sqrt(dble(n)))
end subroutine tstat_f
)---")

system("R CMD SHLIB tstat_f.f90")
dyn.load(paste0("tstat_f", .Platform$dynlib.ext))
tstat_F <- function(x, mu_0) {
  .Fortran("tstat_f", n = length(x), x = as.double(x), mu0 = as.double(mu_0),
    t = 0, PACKAGE = "tstat_f")$t
}
tstat_F(x, mu_0 = 2)


## 3.3 Comparing the speed

if (!requireNamespace("microbenchmark", quietly = TRUE)) install.packages("microbenchmark")
library(microbenchmark)
set.seed(5400)
x <- rnorm(10)
microbenchmark(tstat_R(x, 0), tstat_C(x, 0), tstat_F(x, 0), check = "equal")

x <- rnorm(1000)
microbenchmark(tstat_R(x, 0), tstat_C(x, 0), tstat_F(x, 0), check = "equal")


## 3.4 R packages with C++

d <- read.dcf("pvalDist/DESCRIPTION")
d[, "Version"] <- "0.0.2"
write.dcf(d, "pvalDist/DESCRIPTION")

proj_set("pvalDist")
use_rcpp()

file.copy("tstat_C.cpp", "pvalDist/src/tstat_C.cpp")
Rcpp::compileAttributes("pvalDist")
document("pvalDist")

system("R CMD build pvalDist")
system("R CMD INSTALL pvalDist_0.0.2.tar.gz")
system("R CMD check pvalDist_0.0.2.tar.gz")

library(pvalDist)
packageVersion("pvalDist")
tstat_C(c(1, 2, 3, 5), mu_0 = 2)


## 3.5 R packages with Fortran

d <- read.dcf("pvalDist/DESCRIPTION")
d[, "Version"] <- "0.0.3"
write.dcf(d, "pvalDist/DESCRIPTION")
file.copy("tstat_f.f90", "pvalDist/src/tstat_f.f90")

cat(file = "pvalDist/R/tstat_F.R", r"---(#' One-sample t statistic (Fortran)
#'
#' @param x A numeric vector.
#' @param mu_0 The population mean under the null hypothesis.
#' @return The t statistic.
#' @examples
#' tstat_F(c(1, 2, 3, 5), mu_0 = 2)
#' @export
tstat_F <- function(x, mu_0) {
  .Fortran("tstat_f", n = length(x), x = as.double(x), mu0 = as.double(mu_0),
    t = 0, PACKAGE = "pvalDist")$t
}
)---")

cat(file = "pvalDist/src/init.c", r"---(#include <R.h>
#include <Rinternals.h>
#include <R_ext/Rdynload.h>

/* the C++ routine made by Rcpp */
extern SEXP _pvalDist_tstat_C(SEXP xSEXP, SEXP mu_0SEXP);

/* the Fortran subroutine */
extern void F77_NAME(tstat_f)(int *n, double *x, double *mu0, double *t);

static const R_CallMethodDef CallEntries[] = {
  {"_pvalDist_tstat_C", (DL_FUNC) &_pvalDist_tstat_C, 2},
  {NULL, NULL, 0}
};

static const R_FortranMethodDef FortranEntries[] = {
  {"tstat_f", (DL_FUNC) &F77_NAME(tstat_f), 4},
  {NULL, NULL, 0}
};

void R_init_pvalDist(DllInfo *dll) {
  R_registerRoutines(dll, NULL, CallEntries, FortranEntries, NULL);
  R_useDynamicSymbols(dll, FALSE);
}
)---")

Rcpp::compileAttributes("pvalDist")
document("pvalDist")
system("R CMD build pvalDist")
system("R CMD INSTALL pvalDist_0.0.3.tar.gz")
system("R CMD check pvalDist_0.0.3.tar.gz")

library(pvalDist)
packageVersion("pvalDist")
x <- c(1, 2, 3, 5)
tstat_C(x, mu_0 = 2)
tstat_F(x, mu_0 = 2)
set.seed(5400)
p <- pvalDist2(n = 10, dist = "exp", mu_0 = 2, B = 1000, rate = 1/2)
mean(p < 0.05)
