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
# Check the small root by putting it back in the equation: a*r**2 + b*r + c
# should be near zero, not near 0.25.
import math


def QuadraticSolver(a, b, c):
    discrim = b * b - 4 * a * c
    if discrim < 0:
        sol = [None, None]
        errflag = 1
    else:
        if a != 0:
            root1 = (-b + math.sqrt(discrim)) / (2 * a)
            root2 = (-b - math.sqrt(discrim)) / (2 * a)
            sol = [root1, root2]
            errflag = 0
        else:
            sol = [None, None]
            errflag = 2
    return sol, errflag


def residual(a, b, c, r):
    return a * r**2 + b * r + c


r = QuadraticSolver(1, 1e8, 1)[0][0]
print(r)
print(residual(1, 1e8, 1, r))
