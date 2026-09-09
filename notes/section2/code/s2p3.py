# STAT:5400 Section 2.3 — Functions, Loops, and Plots
# Code from the lecture notes; no output, no solutions.

## 1.1 Write your own functions

import math
def myfunc(x):
  return math.sin(x)
myfunc

import inspect
print(inspect.signature(myfunc))     # formals
print(myfunc.__code__)               # body, already compiled
print(myfunc.__globals__ is globals())  # environment


## 1.2 Quadratic equation solver (a bad example)

import math
def quadratic(a, b, c):
  discrim = b * b - 4 * a * c
  solve = [(-b + m * math.sqrt(discrim)) / (2 * a) for m in (1, -1)]
  return solve

# usage
quadratic(2, 4, 1)


## 1.3 Quadratic equation solver (a better example)

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

QuadraticSolver(2, 4, 1)


## 1.4 A bug the flags do not catch

r = QuadraticSolver(1, 1e8, 1)[0]
print(r)
print(r[0] * r[1])   # must be c/a = 1


## 1.5 Putting a function in its own file

from quadratic import QuadraticSolver
QuadraticSolver(2, 4, 1)

argumts = {"a": 2, "b": 4, "c": 1}
QuadraticSolver(**argumts)


## 1.6 Local and global variables (name masking)

y = -1

def myfun1(x=1, y=1):
  y += 1
  return y

def myfun2(x=1):
  y = y + 1
  return y

def myfun3(x=1):
  global y
  y += 1
  return y

print(myfun1(1)); print(y)

print(myfun2(1)); print(y)

print(myfun3(1)); print(y)


## 1.7 A confusing example (function vs variable)

list = [1, 2, 3]
list((4, 5))

del list
list((4, 5))


## 1.8 Lazy evaluation

x = 0
def myfun4(x): print(x)
myfun4(x := 1)
print(x)

x = 0
def myfun6(x): print("")
myfun6(x := 1)
print(x)


## 1.9 Infix and prefix functions

import operator
type(operator.add)

print(operator.add(3, 4))

letters = [chr(i) for i in range(ord("a"), ord("z") + 1)]
print(letters[1])
print(operator.getitem(letters, 1))


## 1.11 Use a clean environment

del myfun1, myfun2


## 2.1 Looping

for i in range(1, 11):
  print(i)

# enumerate is the counterpart of seq_along
for i, ch in enumerate(letters[:10]):
  print(i, ch)

for j in [1, 37, 81]:
  print(j / 2)

i = 1
while 1 :
  print(i)
  i += 1
  if i > 10: break


## 2.2 Comments on the `range` function in Python

import sys
print(sys.version_info.major)
print(sys.getsizeof(range(5400)))


## 2.3 The `apply` family of functions in R

import numpy as np, timeit
setup = "import numpy as np; A = np.arange(1, 1000001).reshape(1000, 1000, order='F')"

print(timeit.timeit("[A[:, i].mean() for i in range(1000)]",
  setup=setup, number=3))

print(timeit.timeit("A.mean(axis=0)", setup=setup, number=3))


## 2.4 `lapply` and `sapply`

l1 = {"a1": [1, 2, 3], "a2": ["a", "b", "c"], "a3": "abc"}
print({k: len(v) for k, v in l1.items()})
print({k: type(v).__name__ for k, v in l1.items()})

print([len(v) for v in l1.values()])
print(list(map(len, l1.values())))

import numpy as np
funcs = [np.mean, np.median, max]
print([f(list(range(1, 11))) for f in funcs])


## 2.5 `Reduce` function in R

import functools, operator, math
n = 10
print(math.factorial(n))
print(functools.reduce(operator.mul, range(1, n + 1)))

from scipy.special import factorial
print(factorial([5, 8, 10]))


## 2.6 How big can a factorial get?

# Chatbot: "Write it recursively, it is cleaner. Big inputs are
# no problem: these languages switch to exact big integers."
import math
print(math.factorial(171))
print(len(str(math.factorial(171))), "digits")

import sys
print(sys.getrecursionlimit())
def fact_rec(n):
  return 1 if n == 0 else n * fact_rec(n - 1)
try:
  fact_rec(2000)
except RecursionError as e:
  print("RecursionError:", e)


## 2.7 Timing the three versions

import functools, operator, math
print(math.factorial(5))

def MyFactorial1(nseq):
  return [math.factorial(x) for x in nseq]

def MyFactorial2(nseq):
  return [functools.reduce(operator.mul,
    range(1, x+1)) for x in nseq]

print(MyFactorial1([5, 10]))
print(MyFactorial2([5, 10]))

import timeit
mysetup = '''
import functools, operator, math
def MyFactorial1(nseq):
  return [math.factorial(x) for x in nseq]
def MyFactorial2(nseq):
  return [functools.reduce(operator.mul,
    range(1, x+1)) for x in nseq]
'''

print(timeit.timeit(setup=mysetup,
  stmt='MyFactorial1([5, 10])', number=10000))

print(timeit.timeit(setup=mysetup,
  stmt='MyFactorial2([5, 10])', number=10000))


## 5.2 Building a data frame

import pandas as pd
statedf = pd.read_csv("data/state.csv")

statedf[["Population", "Area"]].head()


## 5.3 Functions operating on factors

divs = ["New England", "Middle Atlantic", "South Atlantic",
  "East South Central", "West South Central", "East North Central",
  "West North Central", "Mountain", "Pacific"]
regs = ["Northeast", "South", "North Central", "West"]
statedf["div"] = pd.Categorical(statedf["div"], categories=divs)
statedf["reg"] = pd.Categorical(statedf["reg"], categories=regs)

print(statedf["div"].dtype.name)
print(list(statedf["div"].cat.categories))


## 5.5 Using factors for plotting and model fitting

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
statedf.boxplot(column="Population", by="div", ax=ax, rot=90)
plt.show()

fig, ax = plt.subplots(figsize=(6, 4))
statedf.boxplot(column="Population", by="div", ax=ax, rot=90)
fig.savefig("boxplotstate.eps")


## 5.7 Example of high-level function: Plot

fig, ax = plt.subplots()
statedf["div"].value_counts().reindex(divs).plot.bar(ax=ax)
ax.set_title("Number of States per Division")
plt.show()

fig, ax = plt.subplots()
ax.scatter(statedf["Area"], statedf["Population"])
ax.set_xlabel("Area in Square Miles")
ax.set_ylabel("Population in thousands")
plt.show()

pd.plotting.scatter_matrix(statedf, figsize=(7, 7))
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(9, 4))
axes[0].scatter(statedf["Area"], statedf["Population"])
statedf.boxplot(column="Population", by="reg", ax=axes[1], rot=45)
plt.show()


## 5.8 Log scales

fig, ax = plt.subplots()
ax.scatter(statedf["Area"], statedf["Population"])
ax.set_xscale("log")
plt.show()

fig, ax = plt.subplots()
ax.scatter(statedf["Area"], statedf["Population"])
ax.set_xscale("log"); ax.set_yscale("log")
plt.show()


## 5.9 Low-level plotting functions

fig, ax = plt.subplots()
ax.scatter(statedf["Area"], statedf["Population"], alpha=0)
for a, p, ab in zip(statedf["Area"], statedf["Population"],
    statedf["abb"]):
  ax.text(a, p, ab, ha="center", va="center", fontsize=7)
plt.show()

import statsmodels.api as sm
d = statedf.sort_values("Area")
fig, ax = plt.subplots()
ax.scatter(d["Area"], d["Population"])
ax.plot(*sm.nonparametric.lowess(d["Population"], d["Area"],
  frac=2/3).T, label="frac=2/3")
ax.plot(*sm.nonparametric.lowess(d["Population"], d["Area"],
  frac=0.25).T, ls="--", label="frac=1/14")
ax.legend()
plt.show()


## 5.11 `ggplot2` package

from plotnine import ggplot, aes, geom_point, geom_smooth
p = ggplot(statedf, aes("Area", "Population")) + geom_point()
p + geom_smooth(method="lowess", se=False)
