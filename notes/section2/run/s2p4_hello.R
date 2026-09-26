# STAT 5400 - Section 2.4 - your first LLM API call (R, ellmer)
# The key is a Codespaces secret. Never write it in this file.
# Check the OpenAI key (reads ~/.Renviron again, so no restart is needed after you add the key)
if (file.exists("~/.Renviron")) readRenviron("~/.Renviron")
help_url <- "https://boxiang-wang.github.io/stat5400/notes/section2/s2p4.html#setting-up-idas"
if (!nzchar(Sys.getenv("OPENAI_API_KEY"))) {
  message("No OpenAI key found. How to set it up: ", help_url)
} else if (inherits(try(suppressWarnings(readLines(url("https://api.openai.com/v1/models",
             headers = c(Authorization = paste("Bearer", Sys.getenv("OPENAI_API_KEY")))))), silent = TRUE), "try-error")) {
  message("Your OpenAI key did not work. Check it, or see: ", help_url)
}

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
