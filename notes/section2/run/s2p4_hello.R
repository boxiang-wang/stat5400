# STAT 5400 - Section 2.4 - your first LLM API call (R, ellmer)
# The key is a Codespaces secret. Never write it in this file.
library(ellmer)

chat <- chat_openai(model = "gpt-5-nano")     # reads OPENAI_API_KEY
chat$chat("Write a one-sentence bedtime story about a unicorn.")

# Run it again. The answer is different, because the model samples.
chat2 <- chat_openai(model = "gpt-5-nano")
chat2$chat("Write a one-sentence bedtime story about a unicorn.")

# A chat object keeps the conversation, so the second turn remembers the first.
chat3 <- chat_openai(model = "gpt-5-nano")
chat3$chat("Write two sentences about the University of Iowa.")
chat3$chat("What is the name of the university I just mentioned?")

# What it cost, and which model answered.
chat3$get_model()
chat3$get_tokens()

# Another provider, same code: only the address and the model name change.
# The small local model needs no key and runs inside the Codespace.
local <- chat_ollama(model = "llama3.2:1b")
local$chat("Give me 3 distributions in the exponential family.")
