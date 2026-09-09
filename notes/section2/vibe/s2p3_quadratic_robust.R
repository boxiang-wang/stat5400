# STAT 5400 - Section 2.3 - Vibe task
# Open this file in a Codespace (Copilot on) and let the completion help you.
#
# TASK: ask Copilot to make QuadraticSolver robust. Accept its answer, then test it.
#
# Verify with the three cases below. The third one is the one that matters:
#   QuadraticSolver(2, 4, 1)    two ordinary roots
#   QuadraticSolver(0, 5, 1)    a is zero, not a quadratic
#   QuadraticSolver(1, 1e8, 1)  roots near -1e-8 and -1e8
#
# Done when you can say what the model fixed and what it left alone.
# Check the small root by putting it back in the equation: a*r^2 + b*r + c
# should be near zero, not near 0.25.

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

residual <- function(a, b, c, r) a * r^2 + b * r + c

r <- QuadraticSolver(1, 1e8, 1)$solution[1]
print(r, digits = 17)
print(residual(1, 1e8, 1, r))
