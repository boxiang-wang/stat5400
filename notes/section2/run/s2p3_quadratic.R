# Section 2.3 -- the quadratic solver, saved as its own file.
# In R:  source("notes/section2/run/s2p3_quadratic.R")  puts the function in memory.

QuadraticSolver <- function(aval, bval, cval){
  discrim <- bval * bval - 4 * aval * cval
  if (discrim < 0){
    sol <- c(NA, NA)
    errflag <- 1
  } else {
    if (aval != 0) {
      mult <- c(1, -1)
      sol <- (-bval + mult * sqrt(discrim)) / (2 * aval)
      errflag <- 0
    } else {
      sol <- c(NA, NA)
      errflag <- 2
    }
  }
  return(list(solution=sol, errflag=errflag))
}

QuadraticSolver(2, 4, 1)

argumts <- list(aval=2, bval=4, cval=1)
do.call(QuadraticSolver, argumts)
