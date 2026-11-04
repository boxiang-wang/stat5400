# STAT 5400 - Section 5.1 - the smallest agent: one tool, one task (R, ellmer)
# Needs OPENAI_API_KEY in ~/.Renviron or as a Codespaces secret
# (or ANTHROPIC_API_KEY: replace chat_openai by chat_anthropic). Never put a key in this file.
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
