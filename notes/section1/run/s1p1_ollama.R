# STAT 5400 - Section 1.1 - two small models, no API key
# The Codespace has Ollama with qwen2.5:0.5b (Alibaba, 0.5B parameters) and llama3.2:1b (Meta, 1B).
# Start the Ollama server if it is not running yet (needed once per IDAS session)
ollama_up <- function() !inherits(try(suppressWarnings(readLines("http://localhost:11434/api/version")), silent = TRUE), "try-error")
if (!ollama_up()) {
  if (dir.exists("~/classdata/models")) {             # on IDAS: use the class copy of Ollama and its models
    Sys.setenv(PATH = paste0(path.expand("~/classdata/models/ollama/bin:"), Sys.getenv("PATH")),
               OLLAMA_MODELS = path.expand("~/classdata/models/library"), OLLAMA_NOPRUNE = "1")
  }
  if (nzchar(Sys.which("ollama"))) {                  # skip if Ollama is not installed
    system("nohup ollama serve > ~/ollama.log 2>&1 &")  # start it in the background
    for (i in 1:30) if (ollama_up()) break else Sys.sleep(1)
  }
}

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
