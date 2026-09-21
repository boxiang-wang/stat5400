# STAT:5400 Section 2.4 — LLM APIs and Prompting
# Code from the lecture notes; no output, no solutions.

## 2.2 What a token costs

prompt <- "Explain what a p-value means in one sentence for a beginner."

words  <- length(strsplit(prompt, "\\s+")[[1]])
tokens <- round(words / 0.75)
c(words = words, approx_tokens = tokens)

# Edit
price_per_million <- 0.15     # dollars, input tokens; check the current page
calls             <- 500

round(tokens * calls / 1e6 * price_per_million, 4)

book_tokens <- 745 * 500 / 0.75   # pages, words per page, words per token
book_tokens

# dollars per million input tokens, September 2026; these change often
per_million <- c(nano = 0.05, pro = 30.00)

round(book_tokens / 1e6 * per_million, 2)


## 3.1 Hello world

library(ellmer)

chat <- chat_openai(model = "gpt-5-nano")
chat$chat("Write a one-sentence bedtime story about a unicorn.")


## 3.2 The model does not remember earlier calls

library(ellmer)

first <- chat_openai(model = "gpt-5-nano")    # reads OPENAI_API_KEY
first$chat("Write a paragraph about the Department of Statistics and
            Actuarial Science at the University of Iowa.")

second <- chat_openai(model = "gpt-5-nano")   # a brand new conversation
second$chat("What is the name of the university I just mentioned?")

same <- chat_openai(model = "gpt-5-nano")
same$chat("Write two sentences about the University of Iowa.")
same$chat("What is the name of the university I just mentioned?")

# The same test with Claude. Only the function changes, and it needs ANTHROPIC_API_KEY.
# same <- chat_anthropic()
# same$chat("Write two sentences about the University of Iowa.")
# same$chat("What is the name of the university I just mentioned?")


## 3.3 Open-weight models

small <- chat_ollama(model = "llama3.2:1b")      # 1 billion parameters
small$chat("Give me 3 distributions in the exponential family.")

bigger <- chat_ollama(model = "qwen3.5:4b",      # 4 billion parameters, IDAS only
  api_args = list(reasoning_effort = "none"))    # skip the thinking step
bigger$chat("Give me 3 distributions in the exponential family.")


## 4.2 Roles

# Predict
chat_a <- chat_openai(model = "gpt-5-nano",
  system_prompt = "You are a concise tutor.")
chat_a$chat("X follows a Uniform(0, 1). What is its variance?")

chat_b <- chat_openai(model = "gpt-5-nano",
  system_prompt = paste("You are a responsible tutor. Help your student",
                        "but don't tell them the exact answers."))
chat_b$chat("X follows a Uniform(0, 1). What is its variance?")


## 4.3 Conversation state

chat <- chat_openai(model = "gpt-5-nano")
chat$set_turns(list(
  UserTurn("knock knock."),
  AssistantTurn("Who's there?")))
chat$chat("Felix")

chat <- chat_openai(model = "gpt-5-nano")
chat$chat("Tell me a joke about statistics.")
chat$chat("Tell me another.")
chat$get_turns()    # every turn so far: user, assistant, user, assistant


## 5.1 Ask for a type, not a string

review <- type_object(
  label     = type_enum("One of Supported, Unsupported, Unclear.",
                        c("Supported", "Unsupported", "Unclear")),
  reason    = type_string("One short sentence."),
  p_value   = type_number("The p-value mentioned, or -1 if none."))

chat <- chat_openai(model = "gpt-5-nano")
chat$chat_structured(
  "This study proves the two groups differ (p = 0.20).",
  type = review)


## 6.2 Watch a small model fail, then fix it

library(ellmer)

# no tool: the model answers from text alone
bare <- chat_ollama(model = "llama3.2:1b")
bare$chat("Which is larger, 9.9 or 9.11? Answer with just the number.")

# one tool: now the comparison happens in R
larger <- function(a, b) {
  a <- as.numeric(a); b <- as.numeric(b)         # small models sometimes send "9.9" as text
  if (a > b) a else if (b > a) b else "equal"
}

armed <- chat_ollama(model = "llama3.2:1b",
  system_prompt = "Use the tool to compare numbers. Never compare them yourself.")
armed$register_tools(list(
  tool(larger, "Return the larger of two numbers.",
       arguments = list(a = type_number("First number."),
                        b = type_number("Second number.")))))
armed$on_tool_request(function(req) cat("-> ", req@name, deparse1(req@arguments), "\n"))
armed$chat("Which is larger, 9.9 or 9.11?")


## 6.3 A two-tool example

library(ellmer)
Cars <- read.delim("notes/section2/data/Cars.dat")

column_names <- function() paste(names(Cars), collapse = ", ")
column_mean  <- function(column) mean(Cars[[column]])

chat <- chat_openai(model = "gpt-5-nano",
  system_prompt = "Use the tools to compute. Never guess a number.")

chat$register_tools(list(
  tool(column_names,
       "List the column names of the cars data set. Call this first if unsure.",
       arguments = list()),
  tool(column_mean,
       "Return the mean of one numeric column of the cars data set.",
       arguments = list(column = type_string("Exact column name.")))))

chat$on_tool_request(function(req)
  cat("-> ", req@name, deparse1(req@arguments), "\n"))

chat$chat("What is the average weight of these cars?")
