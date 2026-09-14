# STAT 5400 - Section 2.4 - giving the model a function to call (R, ellmer)
# Two tools, one question. The model must look up the column names before it can compute.
library(ellmer)

# ---- warm-up: a small model cannot compare two numbers, until you give it a tool ----
bare <- chat_ollama(model = "llama3.2:1b")
bare$chat("Which is larger, 9.9 or 9.11? Answer with just the number.")

larger <- function(a, b) if (a > b) a else if (b > a) b else "equal"

armed <- chat_ollama(model = "llama3.2:1b",
  system_prompt = "Use the tool to compare numbers. Never compare them yourself.")
armed$register_tools(list(
  tool(larger, "Return the larger of two numbers.",
       arguments = list(a = type_number("First number."), b = type_number("Second number.")))))
armed$on_tool_request(function(req) cat("-> ", req@name, deparse1(req@arguments), "\n"))
armed$chat("Which is larger, 9.9 or 9.11?")

# ---- the main example: two tools on the cars data ----
Cars <- read.delim("notes/section2/data/Cars.dat")

column_names <- function() paste(names(Cars), collapse = ", ")
column_mean  <- function(column) mean(Cars[[column]])

chat <- chat_openai(model = "gpt-5-nano",
  system_prompt = "Use the tools to compute. Never guess a number.")

chat$register_tools(list(
  tool(column_names,
       "List the column names of the cars data set. Call this first if you are unsure of a name.",
       arguments = list()),
  tool(column_mean,
       "Return the mean of one numeric column of the cars data set.",
       arguments = list(column = type_string("Exact column name, as returned by column_names.")))))

# the receipt: every request and every result, as they happen
chat$on_tool_request(function(req) cat("-> ", req@name, deparse1(req@arguments), "\n"))
chat$on_tool_result(function(res) cat("<- ", deparse1(res@value), "\n"))

chat$chat("What is the average weight of these cars?")

# check the agent against the one line you could have written yourself
mean(Cars$Weight)
