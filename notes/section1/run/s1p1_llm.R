# STAT 5400 - Section 1.1 - Your first LLM API call (R, ellmer)
# Needs GEMINI_API_KEY in the environment (Codespaces secret). Never put the key in this file.
library(ellmer)

models_google_gemini()         # models your key can use; pick a "flash" one if the default is busy (HTTP 503)
chat <- chat_google_gemini(model = "gemini-3.7-flash")   # reads GEMINI_API_KEY
chat$chat("In one sentence, what does a statistician do that a chatbot cannot?")

# Run it again: is the answer identical? (An LLM is a sampler.)
chat2 <- chat_google_gemini(model = "gemini-3.7-flash")
chat2$chat("In one sentence, what does a statistician do that a chatbot cannot?")
