# STAT:5400 Section 2.3 — Functions, Loops, and Plots
# Code from the lecture notes; no output, no solutions.

## 1.1 Write your own functions

myfunc <- function(x) sin(x)
myfunc

formals(myfunc)
body(myfunc)
environment(myfunc)


## 1.2 Quadratic equation solver (a bad example)

quadratic <- function(a, b, c){
  discrim <- b * b - 4 * a * c
  mult <- c(1, -1)
  solve <- (-b + mult * sqrt( discrim ) ) / (2 * a)
   return(solve)
}

# usage
quadratic(2, 4, 1)


## 1.3 Quadratic equation solver (a better example)

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


## 1.4 A bug the flags do not catch

# Predict
r <- QuadraticSolver(1, 1e8, 1)$solution
r
prod(r)   # must be c/a = 1


## 1.5 Putting a function in its own file

source("quadratic.R")
QuadraticSolver(2, 4, 1)

argumts <- list(aval=2, bval=4, cval=1)
do.call(QuadraticSolver, argumts)


## 1.6 Local and global variables (name masking)

y <- -1

myfun1 <- function(x=1, y=1) {
  y <- y + 1; return(y)
}

myfun2 <- function(x=1) {
  y <- y + 1; return(y)
}

myfun3 <- function(x=1) {
  y <<- y + 1; return(y)
}

myfun1(1); print(y)

myfun2(1); print(y)

myfun3(1); print(y)


## 1.7 A confusing example (function vs variable)

c <- 1
c(c = c)


## 1.8 Lazy evaluation

x <- 0
myfun4 <- function(x) print(x)
myfun4(x<-1)
x

x <- 0
myfun5 <- function(x) print(x)
myfun5(x=1)
x

x <- 0
myfun6 <- function(x) print("")
myfun6(x<-1)
x


## 1.9 Infix and prefix functions

class(`+`)

`+`(3, 4)

letters[2]
`[`(letters, 2)


## 1.10 Writing your own infix functions

`%+%` <- function(c1, c2) paste(c1, c2)

"Hawkeye" %+% "State"
"STAT" %+% 5400

`%**%` <- function(c1, i)
  paste(rep(c1, i), collapse=", ")
"Olay" %**% 3


## 1.11 Use a clean environment

rm(list=ls())


## 2.1 Looping

for (i in 1:10) print(i)

for (i in seq_along(letters[1:10])) print(i)

# "for" itself is essentially a function
`for`(i, 1:10, print(i))

for (j in c(1, 37, 81)) print( j/2 )

# while loop: don't know # of iterates in advance
i = 1
while (1) {
  print(i)
  i <- i + 1
  if (i > 10) break
}


## 2.2 Comments on the `range` function in Python

object.size(1:5400)
object.size(seq(5400))


## 2.3 The `apply` family of functions in R

# By hand
# Chatbot: "Use apply(A, 2, mean). apply is vectorised, so it runs at C
# speed and is much faster than writing the loop yourself. colMeans is
# just a convenience wrapper around apply."
A <- matrix(1:1000000, 1000, 1000)
system.time(apply(A, 2, mean))
system.time(colMeans(A))

A <- matrix(1:1000000, 1000, 1000)

system.time(apply(A, 2, mean))

system.time(for(i in 1:1000) mean(A[,i]))

system.time(colMeans(A))


## 2.4 `lapply` and `sapply`

l1 <- list(a1=1L:3L, a2=letters[1:3], a3="abc")
lapply(l1, length)
lapply(l1, typeof)

unlist(lapply(l1, length))
sapply(l1, length)

funcs = list(mean, median, max)
lapply(funcs, function(f) f(1:10))


## 2.5 `Reduce` function in R

n <- 10
factorial(n)
Reduce('*', seq(n))

factorial(c(5, 8, 10))


## 2.6 How big can a factorial get?

# By hand
# Chatbot: "Write it recursively, it is cleaner. Big inputs are
# no problem: these languages switch to exact big integers."
factorial(170)
factorial(171)
prod(1:171)

# how deep R lets calls nest before it stops
getOption("expressions")


## 2.7 Timing the three versions

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


## 5.1 The `state` data

help(state, package="datasets")


## 5.2 Building a data frame

data(state)
statedf <- data.frame(abb=state.abb,
  div=state.division,
  reg=state.region,
  state.x77[ ,c("Population", "Area")])

head(statedf[, c("Population", "Area")])


## 5.3 Functions operating on factors

is.factor(statedf[, "div"])
levels(statedf[, "div"])


## 5.4 Group summaries by a factor

tapply(statedf[, "Population"], statedf[, "reg"], mean)


## 5.5 Using factors for plotting and model fitting

boxplot(Population ~ div, data=statedf)
boxplot(Population ~ div, data=statedf,
  pars=list(cex.axis=0.75))

dev.copy2eps(file="boxplotstatepop.eps", horizontal=T)

setEPS()
postscript(file="boxplotstate", height=4, width=6)
boxplot(Population ~ div, data=statedf)
dev.off()


## 5.7 Example of high-level function: Plot

plot(statedf[,"div"], cex.axis=0.75,
  main="Number of States per Division")

plot( statedf[,"Area"], statedf[,"Population"],
  xlab="Area in Square Miles",
  ylab="Population in thousands")

plot(statedf)

par(mfrow=c(1,2))
plot(Population ~ Area + reg, data=statedf)


## 5.8 Log scales

plot(state.x77[,"Area"],
  state.x77[,"Population"], log="x")

plot(state.x77[,"Area"],
  state.x77[,"Population"], log="xy")


## 5.9 Low-level plotting functions

attach(statedf)
plot(Area, Population, type="n")
text(Area, Population, abb)
detach(statedf)

statedf = statedf[order(statedf[,"Area"]), ]
attach(statedf)
plot(Area, Population)
lines(lowess(Population ~ Area))
lines(lowess(Population ~ Area, f=0.25), lty=2)
legend(400000, 15000,
  legend=c("f=2/3","f=1/14"), lty=1:2)
detach(statedf)


## 5.10 Interactive graphic functions

text(locator(2), "Outlier")


## 5.11 `ggplot2` package

library(ggplot2)
p <- ggplot(statedf, aes(Area, Population)) +
  geom_point()
p + geom_smooth(method="loess", se=FALSE)
