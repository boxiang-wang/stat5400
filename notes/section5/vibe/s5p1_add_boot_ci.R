# STAT 5400 - Section 5.1 - Vibe task: add a third tool to the bootstrap agent
# Open this file in the Codespace. Ask Copilot (chat or inline) for the function boot_ci below.
# Then write the scripted step yourself, run the whole file, and read the receipt.
# Done when the receipt has four rows and the last one is an interval from about 47 to about 187.

aircondit <- c(3, 5, 7, 18, 43, 85, 91, 98, 100, 130, 230, 487)   # hours between failures, HW 9

describe <- function(name) {
  x <- get(name)
  sprintf("%d values; mean %.1f; median %.1f", length(x), mean(x), median(x))
}

# set the seed for one computation only, then put the random number state back
with_seed <- function(seed, expr) {
  old <- if (exists(".Random.seed", globalenv())) get(".Random.seed", globalenv())
  set.seed(seed)
  on.exit(if (!is.null(old)) assign(".Random.seed", old, globalenv()))
  expr
}

boot_se <- function(name, stat, B = 2000, seed = 5400) {
  x <- get(name)
  f <- match.fun(stat)
  est <- with_seed(seed, replicate(B, f(sample(x, replace = TRUE))))
  c(estimate = f(x), se = sd(est))
}

# ---- 1. ask Copilot for this function ----
# Prompt to try: "Write an R function boot_ci(name, stat, B = 2000, seed = 5400) that gets the vector
# by name with get(), draws B bootstrap samples with replacement inside with_seed(seed, ...), applies the
# statistic named by stat to each, and returns c(lower = , upper = ) with the 2.5% and 97.5% quantiles."
boot_ci <- function(name, stat, B = 2000, seed = 5400) {
  c(lower = 0, upper = 0)                        # <- replace with Copilot's function
}

tools <- list(describe = describe, boot_se = boot_se, boot_ci = boot_ci)   # the third tool is registered here

# ---- the loop, the same as on the page ----
show_result <- function(r) {
  if (is.character(r)) return(paste(r, collapse = " "))
  paste(names(r), signif(r, 4), sep = " = ", collapse = ", ")
}

run_agent <- function(model, tools, task, max_steps = 6) {
  history <- task
  receipt <- list()
  for (step in seq_len(max_steps)) {
    action <- model(history, names(tools))
    if (!is.null(action$final)) {
      receipt[[step]] <- data.frame(step, tool = "(answer)", args = "", result = action$final)
      return(list(answer = action$final, receipt = do.call(rbind, receipt), steps = step))
    }
    result <- tryCatch(do.call(tools[[action$tool]], action$args),
                       error = function(e) paste("ERROR:", conditionMessage(e)))
    shown <- show_result(result)
    receipt[[step]] <- data.frame(step, tool = action$tool, args = deparse1(action$args), result = shown)
    history <- c(history, paste0(action$tool, ": ", shown))
  }
  list(answer = NA, receipt = do.call(rbind, receipt), steps = max_steps)
}

# ---- 2. write the third scripted step yourself (no AI for this part) ----
scripted2 <- function(history, tool_names) {
  done <- length(history) - 1
  if (done == 0) return(list(tool = "describe", args = list(name = "aircondit")))
  if (done == 1) return(list(tool = "boot_se",
    args = list(name = "aircondit", stat = "mean", B = 2000)))
  # if (done == 2) return(list(tool = "boot_ci", args = list(...)))   # <- fill in
  list(final = paste("95% percentile interval for the mean:", tail(history, 1)))
}

# ---- 3. run it and read the receipt ----
out2 <- run_agent(scripted2, tools, "Give a 95% percentile bootstrap interval for the mean failure time.")
out2$receipt
