# STAT:5400 Tech Guide 2 — Parallel Computing
# Code from the lecture notes; no output, no solutions.

parallel::detectCores()


## 1 Introduction to the `parallel` package

library(parallel)
cl <- makeCluster(5)
do.call("rbind", clusterCall(cl, function(cl) Sys.info()["nodename"]))


## 1.1 Cluster-level functions

clusterCall(cl, exp, 1)

clusterEvalQ(cl, library(boot))

clusterApply(cl, 1:3, get("+"), 3)

x <- 2; y <- 1
clusterExport(cl, c("x", "y"))
clusterApply(cl, 1:3, function(a) a^x + a * y)


## 1.2 `parLapply`

x <- 1:1000 / 1001
system.time(qtukey(x, 2, df = 2))
system.time(unlist(parLapply(cl, x, qtukey, 2, df = 2)))


## 1.3 Apply-type functions

x <- 2; y <- 1
clusterExport(cl, c("x", "y"))
parSapply(cl, 1:3, function(a) a^x + a * y)
parApply(cl, matrix(1:10, ncol = 2), 2, sum)

(A <- matrix(c(1, 2, 3, 4, 5, 6), nrow = 2))
parCapply(cl, A, sum)
parRapply(cl, A, sum)


## 1.4 A real example: bootstrap

library(profvis)
library(boot)
law <- read.csv("https://boxiang-wang.github.io/stat5400/notes/section4/data/law.csv")

p <- profvis({
  t1 <- Sys.time()
  # estimate cor and the variance of the bootstrap replicates
  mean.se <- function(x, i) {
    corfun <- function(x, i) cor(x$LSAT[i], x$GPA[i])
    v <- var(boot(data = x[i, ], statistic = corfun, R = 2000)$t)
    c(corfun(x, i), v)
  }
  boot.obj <- boot(data = law, statistic = mean.se, R = 200)
  boot.ci(boot.obj, type = "all")
  t2 <- Sys.time()
  difftime(t2, t1, unit = "sec")
})
p
htmlwidgets::saveWidget(p, "profile.html", selfcontained = FALSE)

invisible(clusterEvalQ(cl, {
  library(boot)
  law <- read.csv("https://boxiang-wang.github.io/stat5400/notes/section4/data/law.csv")
  # estimate cor and the variance of the bootstrap replicates
  mean.se <- function(x, i) {
    corfun <- function(x, i) cor(x$LSAT[i], x$GPA[i])
    v <- var(boot(data = x[i, ], statistic = corfun, R = 2000)$t)
    c(corfun(x, i), v)
  }
}))
clusterSetRNGStream(cl, 5400)
t1 <- Sys.time()
res <- clusterEvalQ(cl, boot(data = law, statistic = mean.se, R = 40))
cl_boot <- do.call(c, res)
boot.ci(cl_boot, type = c("norm", "basic", "perc", "stud"))
t2 <- Sys.time()
difftime(t2, t1, unit = "sec")

cl_boot_func <- function(...) {
  library(boot)
  law <- read.csv("https://boxiang-wang.github.io/stat5400/notes/section4/data/law.csv")
  mean.se <- function(x, i) {
    corfun <- function(x, i) cor(x$LSAT[i], x$GPA[i])
    v <- var(boot(data = x[i, ], statistic = corfun, R = 2000)$t)
    c(corfun(x, i), v)
  }
  boot(data = law, statistic = mean.se, R = 40)
}
clusterSetRNGStream(cl, 5400)
t1 <- Sys.time()
cl_boot <- do.call(c, parLapply(cl, seq_along(cl), cl_boot_func))
boot.ci(cl_boot, type = c("norm", "basic", "perc", "stud"))
t2 <- Sys.time()
difftime(t2, t1, unit = "sec")

stopCluster(cl)


## 1.5 `foreach`

library(doParallel)
library(foreach)
cl <- makeCluster(3)
registerDoParallel(cl)
foreach(i = 1:3) %dopar% sqrt(i)
foreach(i = 1:3, .combine = c, .errorhandling = "pass") %dopar% {
  sqrt(i)
}
stopCluster(cl)


## 2 Distributed learning

ids <- 1:10
all_boot <- vector("list", length(ids))
# get the boot object from each R image
for (ii in seq_along(ids)) {
  load(paste0("image_", ids[ii], ".RData"))
  all_boot[[ii]] <- boot.obj
}
# combine them together and get the bootstrap CI
library(boot)
all_boot_c <- do.call(c, all_boot)
all_boot_c$R
boot.ci(all_boot_c, type = c("norm", "basic", "perc", "stud"))
