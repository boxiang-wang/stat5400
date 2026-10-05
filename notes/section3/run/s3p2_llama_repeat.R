# STAT 5400 - Section 3.2 - ask llama3.2:1b the same question 50 times, then a CI for P(correct)
# Runs on IDAS (RStudio) or in the Codespace. No API key needed. Takes about a minute.

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

q <- "Which is larger, 9.9 or 9.11? Answer with the number only."
answers <- character(50)
for (i in 1:50) {
  answers[i] <- trimws(chat_ollama(model = "llama3.2:1b")$chat(q, echo = "none"))   # a new chat each time
}
table(answers)

x <- sum(answers == "9.9")                        # number of correct answers
x
prop.test(x, 50, correct = FALSE)$conf.int         # Wilson interval
binom.test(x, 50)$conf.int                        # Clopper-Pearson (exact) interval
