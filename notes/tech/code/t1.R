# STAT:5400 Tech Guide 1 — Linux and the lnx Machines
# Code from the lecture notes; no output, no solutions.

## 10.1 Several jobs at once

nlist <- c(10, 20, 50, 100, 200)
files <- paste0("TypeIerr_", nlist, "_exp.RData")
res <- sapply(files, function(f) { load(f); TypeIerr })
names(res) <- nlist
res
