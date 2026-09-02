# STAT:5400 Section 2.1 — A First Look at R
# Code from the lecture notes; no output, no solutions.

## 1.5 Basic operation

1 + 1
exp(-2)
sqrt(2 * pi)

2 / 0
3 / 2 * 3

print("Hello 5400!")

# Predict
0.1 + 0.2 == 0.3
all.equal(0.1 + 0.2, 0.3)
.Machine$double.eps

# Predict
1:3 + 1:2
1:4 + 1:2


## 1.6 Reading in data from external files

Cars <- read.delim("data/Cars.dat")
#  <- is assignment operator
str(Cars)

# show the first six rows
head(Cars)

# show the last six rows
tail(Cars)

summary(Cars)

plot(Cars)


## 1.7 Data frames

class(Cars)


## 2.2 Vectors

a1 <- c(1, 2, 3)
class(a1)
typeof(a1)
is.integer(a1)
is.atomic(a1)

a2 <- c(1L, 2L, 3L)
# same to a2 <- seq(3) or seq.int(3)
class(a2)
typeof(a2)

a3 <- c(T, F, TRUE, FALSE) # ALWAYS spell T and F.
class(a3); typeof(a3) # semicolons not recommended.
as.numeric(a3)

# Predict
T <- FALSE
c(T, TRUE)
rm(T)     # put things back
T

a4 <- c("T", "F")
class(a4); typeof(a4)
as.numeric(a4)

a5 <- c(T, F, "T", "F")
typeof(a5)


## 2.3 Lists

l1 <- list(c(1, 2), c(T, F), c("T", "F"), 1 + 2)
str(l1)
unlist(l1)

l2 <- list(list(), list(list()))
str(l2)


## 2.4 Three properties of vectors and lists

a1 <- c(T, T, F)
l1 <- list(T, T, 2)
names(a1) <- names(l1) <- paste0("name", 1:3)

a1

l1$name2
l1[2]

length(a1); length(l1)

attr(a1, "my_attr") <- "This is my vector."
attributes(a1)
a1


## 2.5 Factors

x <- factor(c("S", "T", "A", "T"))
x

is.atomic(x)
is.factor(x)

attributes(x)
levels(x)

is.factor(Cars$Country)
Cars$Country <- factor(Cars$Country)
levels(Cars$Country)

boxplot(Cars$MPG ~ Cars$Country)

# Predict
f <- factor(c("10", "9", "8"))
as.numeric(f)

as.numeric(as.character(f))   # 10 9 8


## 2.6 Matrices and arrays

a <- matrix(1:6, ncol = 3, nrow = 2)
b <- array(1:12, c(2, 3, 2))

b <- 1:12
dim(b) <- c(2, 3, 2)

rownames(a) <- c("row1", "row2")
colnames(a) <- paste0("col", 1:3)
dimnames(b) <- list(letters[1:2], LETTERS[1:3],
  c("one", "two"))

# a
# b


## 2.7 Data frames

dat <- data.frame(x1 = 2:4, x2 = letters[1:3])
str(dat)

dat2 <- data.frame(x1 = 2:4, x2 = letters[1:3],
  stringsAsFactors = FALSE)
str(dat2)

is.list(Cars)
dim(Cars)

is.data.frame(Cars)
str(Cars)


## 3.1 Subsetting a vector

(x <- 1:4 * 10)
x[c(1, 3)] # assign values: x[c(1, 3)] <- c(1, 2)

x[order(x)]
x[c(1, 1)]
x[c(1.2, 2.9)]

x[-c(3, 1)]
x[c(-3, 1)]

x[x < 25]
which(x < 25)

x[c(TRUE, FALSE, TRUE, TRUE)]
x[c(TRUE, FALSE)]

x[c(TRUE, FALSE, TRUE, TRUE, TRUE)]
x[c(TRUE, FALSE, NA, TRUE)]

names(x) <- letters[1:4]
x[c("a", "c")]

# By hand
# Chatbot: "Logical subsetting keeps the elements marked TRUE. The index
# here has only two values, so R uses them for the first two elements and
# ignores the rest. v[c(TRUE, FALSE)] therefore returns the first element,
# a vector of length 1."
v <- 1:6 * 5
v[c(TRUE, FALSE)]


## 3.2 Subsetting a list

l1 <- list(a = 1, b = 2, c = 3)

l1$a
l1[[1]]
l1[1]


## 3.3 Words on the `drop` option

f1 <- factor(c("s", "t", "a", "t"))
f1[1:2]
f1[1:2, drop = TRUE]

a <- matrix(1:8, 2, 4)
colMeans(a[, 1:2])
a[, 1]

colMeans(a[, 1])

a[, 1, drop = FALSE]
colMeans(a[, 1, drop = FALSE])


## 4.1 Subsetting rows and columns of a data frame

Cars[1:6, ]

head(Cars[, c("Country", "MPG", "Weight")])

head(Cars[Cars$Country == "U.S.", ])

head(Cars[Cars$Country == "Japan", ])

table(Cars$Country)
summary(Cars[Cars$Country == "U.S.", "MPG"])
summary(Cars[Cars$Country == "Japan", "MPG"])

hist(Cars[Cars$Country == "U.S.", "MPG"])

hist(Cars[Cars$Country == "Japan", "MPG"])


## 4.2 One-sample t-test

t.test(Cars[Cars$Country == "U.S.", "MPG"])

UStout <- t.test(Cars[Cars$Country == "U.S.", "MPG"])
names(UStout)

UStout$conf.int
UStout$estimate
UStout$statistic

t.test(Cars[Cars$Country == "Japan", "MPG"])


## 4.3 Two-sample t-test

t.test(Cars[Cars$Country == "U.S.", "MPG"],
  Cars[Cars$Country == "Japan", "MPG"])
