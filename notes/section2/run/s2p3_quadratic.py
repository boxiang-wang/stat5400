# Section 2.3 -- the quadratic solver, saved as its own file.
# In Python:  from quadratic import QuadraticSolver   (rename this file quadratic.py first),
# or run it once with:  exec(open("notes/section2/run/s2p3_quadratic.py").read())
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


if __name__ == "__main__":
    print(QuadraticSolver(2, 4, 1))

    argumts = {"a": 2, "b": 4, "c": 1}
    print(QuadraticSolver(**argumts))
