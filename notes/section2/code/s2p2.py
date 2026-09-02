# STAT:5400 Section 2.2 — A First Look at Python
# Code from the lecture notes; no output, no solutions.

## 1.4 Hello 5400!

print('Hello', '5400!')
print('Hello', '5400', end='!\n')
print('Hello' + ' ' + '5400')


## 1.6 Basic operations in Python

1 + 1

exp(-2)

import math
from math import *

from math import exp, sqrt, pi
print(exp(-2))
print(sqrt(2 * pi))

2 / 0


## 1.7 Integers and floats

# Predict
print(3 / 2 * 3)
print(3 // 2 * 3)
print(3.0 / 2 * 3)


## 2.2 The library `pandas`

import pandas as pd
Cars = pd.read_csv('data/Cars.dat', sep='\t')
Cars.dtypes


## 2.3 The first rows

Cars.head(2)


## 2.4 Summaries

Cars[['Country', 'MPG']].describe(include='all')


## 2.5 All pairs

import matplotlib.pyplot as plt
import seaborn as sns
sns.pairplot(Cars, hue='Country')
plt.show()


## 2.6 Data frames

type(Cars)


## 2.7 Vectors

print(type(1))
print(type(1.0))
print(type(True))
print(type('True'))

print(not True)
print(type(1 - 1j))


## 2.8 Vectors and lists

x = [5, 4, 0, 0]
print(x)

y = ['Hello', '5400']
print(y)
print([y, '!'])

y.append('!')
print(y)

# Chatbot: "b = a makes b a copy of the list, so the two are independent.
# Appending to b leaves a unchanged, and a still prints [1, 2, 3]."
a = [1, 2, 3]
b = a
b.append(4)
print(a)

y = ['Hello', '5400']
z = {'word': y, 'sign': '!'}
print(z)

print(z['word'])
print(z['sign'])


## 2.9 Matrices and arrays

import numpy as np
a = np.reshape(list(range(1, 7)), (2, 3), order='F')
a

b = [1, 2, 3]
np.dot(a, b)


## 2.10 The library `Numpy`

# Predict
import numpy as np
print(list(range(1, 5)) * 3)
print(np.array(range(1, 5)) * 3)


## 3.1 Subsetting a vector

x = np.array(range(1, 6)) * 3
print(x)             # range [start, stop) -- a half-open interval

# Predict
print(x[0:1])        # note Python begins with 0
print(x[0:4:2])
print(np.array(x)[[0, 2]])

import numpy as np
v = np.array(range(1, 7)) * 5
try:
  print(v[np.array([True, False])])
except IndexError as e:
  print("IndexError:", e)

# By hand
# Chatbot: "Slicing a NumPy array returns a copy, just as R does. Writing to
# the slice never touches the original, so a prints [1 2 3 4 5] all three
# times below."
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = a[0:2]
b[0] = 99
print("after a[0:2]   :", a)

a = np.array([1, 2, 3, 4, 5])
c = a[[0, 1]]
c[0] = 99
print("after a[[0,1]] :", a)

a = np.array([1, 2, 3, 4, 5])
m = a[a > 3]
m[0] = 99
print("after a[a > 3] :", a)


## 3.2 Subsetting a matrix

a = np.array([[1, 3, 5, 7], [2, 4, 6, 8]])
print(a[0, ])
print(a[:, 0])

# Predict
print(a.mean(axis=0))
print(a.mean(axis=1))


## 3.3 Strings in Python

s = 'Hello 5400'
print(len(s))
print(s[0])

print(s[0:6:2])
print(s[-1])
print(s[6:-1])

print(s.lower()) # s.upper()

a, b = s.split(' ')
print(a)
print(b)
print(a + b)


## 4.1 Selecting columns

Cars[['Country', 'MPG']].head(5)


## 4.2 Selecting rows

US_Cars = Cars.loc[Cars['Country'] == 'U.S.']
US_Cars[['Country', 'MPG']].head(5)

JPN_Cars = Cars.loc[Cars['Country'] == 'Japan']
JPN_Cars[['Country', 'MPG']].head(5)


## 4.3 Counts and summaries

from collections import Counter
Counter(Cars['Country'])

pd.concat([US_Cars['MPG'],
  JPN_Cars['MPG']], axis=1).describe()


## 4.4 Histograms

import matplotlib.pyplot as plt
plt.hist(US_Cars['MPG'], bins=range(15, 40, 5))
plt.show()


## 4.5 The package `Matplotlib`

import matplotlib.pyplot as plt
plt.hist(JPN_Cars['MPG'], bins=range(15, 40, 5))
plt.show()


## 4.6 One-sample t-test

from scipy.stats import ttest_1samp
t1 = ttest_1samp(US_Cars['MPG'], 20)
print(t1)

print(t1.pvalue)


## 4.7 Two-sample t-test

from scipy.stats import ttest_ind
t2 = ttest_ind(US_Cars['MPG'], JPN_Cars['MPG'],
  equal_var=False)
print(t2)

print(t2.pvalue)
