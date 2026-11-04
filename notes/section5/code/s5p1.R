# STAT:5400 Section 5.1 — AI Agents
# Code from the lecture notes; no output, no solutions.

if (dir.exists("~/classdata/models/R")) .libPaths(c("~/classdata/models/R", .libPaths()))  # on IDAS: the class copy of ellmer
# Check the OpenAI key (reads ~/.Renviron again, so no restart is needed after you add the key)
if (file.exists("~/.Renviron")) readRenviron("~/.Renviron")
help_url <- "https://boxiang-wang.github.io/stat5400/notes/section2/s2p4.html#setting-up-idas"
if (!nzchar(Sys.getenv("OPENAI_API_KEY"))) {
  message("No OpenAI key found. How to set it up: ", help_url)
} else if (inherits(try(suppressWarnings(readLines(url("https://api.openai.com/v1/models",
             headers = c(Authorization = paste("Bearer", Sys.getenv("OPENAI_API_KEY")))))), silent = TRUE), "try-error")) {
  message("Your OpenAI key did not work. Check it, or see: ", help_url)
}


## 2.1 The smallest agent

library(ellmer)

# 1. a tool: an ordinary R function
run_r <- function(code) paste(capture.output(print(eval(parse(text = code)))), collapse = "\n")

# 2. its description: what the model reads instead of the code
tool_run <- tool(run_r, "Run one piece of R code and return what it prints.",
                 arguments = list(code = type_string("The R code to run.")))

# 3. the model, with instructions, and the tool attached
chat <- chat_openai(system_prompt = "Use the tool to compute. Never guess a number.")
chat$register_tools(list(tool_run))

# 4. print the receipt as it happens
chat$on_tool_request(function(request) cat("-> run_r:", request@arguments$code, "\n"))
chat$on_tool_result(function(result)   cat("<-", result@value, "\n"))

# 5. one task. ellmer runs the loop: ask, act, observe, repeat, until the model answers.
chat$chat("What is the 0.975 quantile of the t distribution with 10 degrees of freedom?")


## 3.1 A stand-in agent, for simulation

aircondit <- c(3, 5, 7, 18, 43, 85, 91, 98, 100, 130, 230, 487)   # hours between failures, HW 9

#' Describe a data vector: its length, mean, and median.
#' Call this before bootstrapping.
#' @param name Name of the vector, for example "aircondit".
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

#' Bootstrap standard error of a statistic of a data vector.
#' @param name Name of the vector.
#' @param stat The statistic: "mean" or "median".
#' @param B Number of bootstrap samples.
#' @param seed Seed for the random numbers, so the result can be repeated.
boot_se <- function(name, stat, B = 2000, seed = 5400) {
  x <- get(name)
  f <- match.fun(stat)
  est <- with_seed(seed, replicate(B, f(sample(x, replace = TRUE))))
  c(estimate = f(x), se = sd(est))
}

tools <- list(describe = describe, boot_se = boot_se)

describe("aircondit")
boot_se("aircondit", stat = "mean", B = 2000)

show_result <- function(r) {
  if (is.character(r)) return(paste(r, collapse = " "))
  paste(names(r), signif(r, 4), sep = " = ", collapse = ", ")
}

run_agent <- function(model, tools, task, max_steps = 6) {
  history <- task
  receipt <- list()
  for (step in seq_len(max_steps)) {
    action <- model(history, names(tools))            # 1. ask the model what to do
    if (!is.null(action$final)) {                     # 2. it answered: stop
      receipt[[step]] <- data.frame(step, tool = "(answer)", args = "",
                                    result = action$final)
      return(list(answer = action$final, receipt = do.call(rbind, receipt), steps = step))
    }
    result <- tryCatch(                               # 3. run the tool it asked for
      do.call(tools[[action$tool]], action$args),
      error = function(e) paste("ERROR:", conditionMessage(e)))
    shown <- show_result(result)
    receipt[[step]] <- data.frame(step, tool = action$tool,
                                  args = deparse1(action$args), result = shown)
    history <- c(history, paste0(action$tool, ": ", shown))  # 4. show the result
  }
  # 5. out of steps
  list(answer = NA, receipt = do.call(rbind, receipt), steps = max_steps)
}

scripted <- function(history, tool_names) {
  done <- length(history) - 1                 # how many tool results so far
  if (done == 0) return(list(tool = "describe", args = list(name = "aircondit")))
  if (done == 1) return(list(tool = "boot_se",
    args = list(name = "aircondit", stat = "mean", B = 2000)))
  list(final = paste("Bootstrap SE of the mean:",
    sub(".*se = ([^,]+).*", "\\1", tail(history, 1))))
}

out <- run_agent(scripted, tools, "Estimate the mean failure time and its bootstrap standard error.")
out$answer

# Predict
out$receipt


## 3.2 An agent's success rate

sloppy <- function(history, tool_names) {
  done <- length(history) - 1
  u <- runif(1)
  if (done == 0) return(list(tool = "describe", args = list(name = "aircondit")))
  if (grepl("ERROR", tail(history, 1)))          # recover from an error
    return(list(tool = "boot_se", args = list(name = "aircondit", stat = "mean", B = 2000)))
  if (done == 1) {
    # answers without bootstrapping
    if (u < 0.10) return(list(final = "Bootstrap SE of the mean: about 40."))
    # the wrong statistic
    if (u < 0.25) return(list(tool = "boot_se",
                              args = list(name = "aircondit", stat = "median", B = 2000)))
    # a typo in the statistic
    if (u < 0.32) return(list(tool = "boot_se",
                              args = list(name = "aircondit", stat = "maen", B = 2000)))
    return(list(tool = "boot_se", args = list(name = "aircondit", stat = "mean", B = 2000)))
  }
  list(final = paste("Bootstrap SE of the mean:",
    sub(".*se = ([^,]+).*", "\\1", tail(history, 1))))
}

set.seed(5400)   # run this block once

run_agent(sloppy, tools, "Estimate the mean failure time and its bootstrap SE.")$receipt


## 3.3 Success rate, with an interval

truth <- unname(boot_se("aircondit", "mean", B = 2000, seed = 5400)["se"])
is_right <- function(answer) {
  s <- suppressWarnings(as.numeric(sub(".*: ", "", answer)))
  isTRUE(abs(s - truth) < 0.05)
}

set.seed(5400)
runs <- replicate(200, {
  r <- run_agent(sloppy, tools, "Estimate the mean failure time and its bootstrap SE.")
  c(ok = is_right(r$answer), steps = r$steps)
})
ok <- runs["ok", ]
mean(ok)

# Wilson interval for the success rate, Section 3.2
prop.test(sum(ok), length(ok), correct = FALSE)$conf.int

table(steps = runs["steps", ])


## 3.4 Audit the agent

# By hand
receipt_1 <- data.frame(
  step = 1:3,
  tool = c("describe", "boot_se", "(answer)"),
  args = c('list(name = "aircondit")',
           'list(name = "aircondit", stat = "median", B = 2000)', ""),
  result = c("12 values; mean 108.1; median 88.0", "estimate = 88, se = 28.78",
             "Bootstrap SE of the mean: 28.78"))
receipt_1

# By hand
receipt_2 <- data.frame(
  step = 1:2,
  tool = c("describe", "(answer)"),
  args = c('list(name = "aircondit")', ""),
  result = c("12 values; mean 108.1; median 88.0",
             "Bootstrap SE of the mean: 39.3 (the standard deviation divided by the square root of 12)"))
receipt_2

# By hand
receipt_3 <- data.frame(
  step = 1:4,
  tool = c("describe", "boot_se", "boot_se", "(answer)"),
  args = c('list(name = "aircondit")',
           'list(name = "aircondit", stat = "mean", B = 2000, seed = 5400)',
           'list(name = "aircondit", stat = "mean", B = 2000, seed = 5400)', ""),
  result = c("12 values; mean 108.1; median 88.0", "estimate = 108.1, se = 36.77",
             "estimate = 108.1, se = 36.77",
             "Bootstrap SE of the mean: 36.77, confirmed by two independent bootstrap runs."))
receipt_3
