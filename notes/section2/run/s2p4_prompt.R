# STAT 5400 - Section 2.4 - roles, few-shot prompting, and structured output (R, ellmer)
library(ellmer)

# ---- roles: the system prompt outranks the user's question ----
chat_a <- chat_openai(model = "gpt-5-nano", system_prompt = "You are a concise tutor.")
chat_a$chat("X follows a Uniform(0, 1). What is its variance?")

chat_b <- chat_openai(model = "gpt-5-nano",
  system_prompt = paste("You are a responsible tutor. Help your student",
                        "but don't tell them the exact answers."))
chat_b$chat("X follows a Uniform(0, 1). What is its variance?")

# ---- few-shot: three examples define the task, with no fitting of any kind ----
INSTRUCTIONS <- "Label short statistical claims as Supported, Unsupported, or Unclear,
based only on the evidence quoted in the claim. Answer with one word.

Examples
Claim: The new drug lowered blood pressure (mean difference -5.2, 95% CI -8.1 to -2.3, p=0.001).
Answer: Supported
Claim: This study proves the two groups are different (mean difference 1.1, 95% CI -0.6 to 2.8, p=0.20).
Answer: Unsupported
Claim: The treatment improved outcomes, but only a trend was observed (p=0.07).
Answer: Unclear"

claims <- c("We can conclude there is no effect because p=0.40.",
            "The results show a significant increase (95% CI 0.1 to 0.4).",
            "The intervention might help, but the CI crosses zero (95% CI -0.2 to 0.3).")

for (cl in claims) {
  chat <- chat_openai(model = "gpt-5-nano", system_prompt = INSTRUCTIONS)
  cat(cl, "\n  ->", chat$chat(cl, echo = "none"), "\n")
}

# ---- structured output: ask for a type, and stop parsing strings ----
review <- type_object(
  label   = type_enum("One of Supported, Unsupported, Unclear.",
                      c("Supported", "Unsupported", "Unclear")),
  reason  = type_string("One short sentence."),
  p_value = type_number("The p-value mentioned in the claim, or -1 if none."))

chat <- chat_openai(model = "gpt-5-nano")
str(chat$chat_structured("This study proves the two groups differ (p = 0.20).", type = review))
