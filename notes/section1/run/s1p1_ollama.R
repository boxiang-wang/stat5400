# STAT 5400 - Section 1.1 - two small models, no API key
# The Codespace has Ollama with qwen2.5:0.5b (Alibaba, 0.5B parameters) and llama3.2:1b (Meta, 1B).
library(ellmer)

q <- "Which is larger, 9.11 or 9.9? Answer in one line."

small <- chat_ollama(model = "qwen2.5:0.5b")
small$chat(q)

bigger <- chat_ollama(model = "llama3.2:1b")
bigger$chat(q)

# Same question five times to the small model. Same answer every time?
for (i in 1:5) print(chat_ollama(model = "qwen2.5:0.5b")$chat("Which is larger, 9.11 or 9.9? Answer with the number only."))

# Compare with Gemini (needs GEMINI_API_KEY):
# chat_google_gemini()$chat(q)
