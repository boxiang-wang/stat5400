# STAT 5400 - Section 5.1 - the bootstrap agent with a real model (R, ellmer)
# The two tools from the page, describe and boot_se, with a real model running the loop.
# Needs OPENAI_API_KEY in ~/.Renviron or as a Codespaces secret
# (or ANTHROPIC_API_KEY: replace chat_openai by chat_anthropic). Never put a key in this file.
library(ellmer)

# ---- the data and the two tools: plain R functions, the same as on the page ----
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

# ---- the same functions, with a description the model can read ----
tool_describe <- tool(describe,
  "Describe a data vector: its length, mean, and median. Call this before bootstrapping.",
  arguments = list(name = type_string("Name of the vector, for example 'aircondit'.")))

tool_boot <- tool(boot_se,
  "Bootstrap standard error of a statistic of a data vector. Returns the estimate and the standard error.",
  arguments = list(
    name = type_string("Name of the vector."),
    stat = type_string("The statistic: 'mean' or 'median'."),
    B    = type_integer("Number of bootstrap samples."),
    seed = type_integer("Seed for the random numbers.")))

# ---- the model, with instructions, and the tools attached ----
chat <- chat_openai(system_prompt = "You are a careful statistical assistant. Use the tools to compute; never guess a number.")
chat$register_tools(list(tool_describe, tool_boot))

# ---- the receipt: every request and every result, as they happen ----
chat$on_tool_request(function(request) cat("->", request@name, deparse1(request@arguments), "\n"))
chat$on_tool_result(function(result)   cat("<-", deparse1(result@value), "\n"))

# ---- one task. ellmer runs the loop: ask, act, observe, repeat, until the model answers ----
chat$chat("Estimate the mean failure time of the aircondit data and its bootstrap standard error with B = 2000.")

# ---- what to hand in ----
chat$get_turns()      # the full transcript
chat$get_tokens()     # tokens used; cost = tokens times the price
record <- list(
  date          = Sys.Date(),
  model         = chat$get_model(),
  settings      = "provider defaults; no temperature set",
  system_prompt = chat$get_system_prompt(),
  tools         = chat$get_tools(),      # the tool definitions
  turns         = chat$get_turns(),      # the full transcript
  tokens        = chat$get_tokens())
saveRDS(record, paste0("agent_run_", Sys.Date(), ".rds"))   # the receipt, on disk
