# STAT 5400 - Section 5.1 - an agent that writes an R package (R, ellmer)
# The same loop as s5p1_agent_ellmer.R, with four tools: write a file, read a file,
# list the files, and run R code. The model decides the steps; the tools carry them out.
# Needs a model that calls tools well. The script picks the first one it finds:
#   OPENAI_API_KEY                   -> chat_openai()
#   ANTHROPIC_API_KEY                -> chat_anthropic()
#   COURSE_MODEL_URL, COURSE_MODEL   -> the course model on IDAS (OpenAI-compatible endpoint)
#   nothing                          -> Ollama llama3.2:1b in the Codespace (too small for this task)
# Set the key once, as a Codespaces secret or in ~/.Renviron. Never put a key in this file.
# Also needs R CMD build and R CMD check (they come with R) and roxygen2 (the agent installs it if missing).

library(ellmer)

# ---- the idea, in one sentence. Change it. ----
idea <- paste(
  "An R package named pvals that computes two-sided p-values from a test statistic:",
  "pval_z(z) for a standard normal statistic, pval_t(t, df) for a t statistic,",
  "and pval_chisq(x, df) for a chi-square statistic (upper tail).")

# ---- the sandbox: the folder the agent works in ----
work <- path.expand(Sys.getenv("PKG_AGENT_DIR", "~/STAT5400/pkg_agent"))
dir.create(work, recursive = TRUE, showWarnings = FALSE)
ASK <- FALSE          # TRUE: you approve every run_r call before it runs (human intervention)

inside <- function(path) {                       # refuse paths that leave the sandbox
  full <- normalizePath(file.path(work, path), mustWork = FALSE)
  if (!startsWith(full, normalizePath(work))) stop("path is outside the sandbox: ", path)
  full
}

# ---- tools: four plain R functions ----
write_file <- function(path, content) {
  full <- inside(path)
  dir.create(dirname(full), recursive = TRUE, showWarnings = FALSE)
  writeLines(content, full)
  sprintf("wrote %s (%d lines)", path, length(strsplit(content, "\n", fixed = TRUE)[[1]]))
}

read_file <- function(path) {
  paste(readLines(inside(path), warn = FALSE), collapse = "\n")
}

list_files <- function() {
  f <- list.files(work, recursive = TRUE, all.files = TRUE, no.. = TRUE)
  f <- f[!grepl("\\.Rcheck/", f)]                 # the check folder is long and not ours
  if (length(f) == 0) "(the sandbox is empty)" else paste(f, collapse = "\n")
}

run_r <- function(code) {
  if (ASK) {
    cat("\n---- the agent wants to run ----\n", code, "\n--------------------------------\n")
    if (tolower(readline("Run it? (y/n) ")) != "y") return("REFUSED: the user did not approve this code.")
  }
  script <- tempfile(fileext = ".R")
  writeLines(code, script)
  old <- setwd(work); on.exit(setwd(old))        # the fresh R session starts in the sandbox
  out <- tryCatch(
    suppressWarnings(                              # a non-zero exit is reported below, not as a warning
      system2(file.path(R.home("bin"), "Rscript"), c("--no-save", "--no-restore", shQuote(script)),
              stdout = TRUE, stderr = TRUE, timeout = 600)),
    error = function(e) paste("ERROR:", conditionMessage(e)))
  status <- attr(out, "status")
  out <- paste(out, collapse = "\n")
  if (nchar(out) > 8000)                           # keep the receipt readable
    out <- paste0(substr(out, 1, 4000), "\n... [", nchar(out) - 8000, " characters cut] ...\n",
                  substr(out, nchar(out) - 3999, nchar(out)))
  if (!nzchar(out)) out <- "(no output)"
  if (!is.null(status) && status != 0) out <- paste0(out, "\n[exit status ", status, "]")
  out
}

# ---- the same functions, with a contract the model can read ----
tool_write <- tool(write_file,
  paste("Write a text file inside the sandbox, creating folders as needed. Overwrites an existing file.",
        "Use it for DESCRIPTION, R/*.R, and any other package file."),
  arguments = list(
    path    = type_string("Path relative to the sandbox, for example 'pvals/R/pvals.R'."),
    content = type_string("The full text of the file.")))

tool_read <- tool(read_file,
  "Read a text file inside the sandbox and return its content.",
  arguments = list(path = type_string("Path relative to the sandbox.")))

tool_list <- tool(list_files,
  "List every file in the sandbox, one per line.")

tool_run <- tool(run_r,
  paste("Run R code in a fresh R session whose working directory is the sandbox.",
        "Returns everything the session printed, including errors.",
        "Use it to document, build, check, and try the package,",
        "for example system('R CMD build pvals')."),
  arguments = list(code = type_string("The R code to run.")))

# ---- the instructions: the third component of an agent ----
instructions <- paste(
  "You are an experienced R package developer. You build a small R package from a one-sentence idea,",
  "inside the sandbox, using only the tools. Work in this order.",
  "1. Write <name>/DESCRIPTION (fields Package, Type, Title, Version 0.1.0, Authors@R, Description,",
  "   License GPL-3, Encoding UTF-8, Imports if the code uses another package, Roxygen: list(markdown = TRUE))",
  "   and <name>/R/<name>.R with the functions and roxygen comments (@param, @return, @examples, @export,",
  "   and @importFrom for every function taken from another package, including stats).",
  "2. Run roxygen2::roxygenise('<name>') to create NAMESPACE and man/. If roxygen2 is missing,",
  "   install it first with install.packages('roxygen2', repos = 'https://cloud.r-project.org').",
  "3. Run system('R CMD build <name>'), then system('R CMD check --no-manual <name>_0.1.0.tar.gz').",
  "4. Read the check output. Fix every ERROR and WARNING, and every NOTE you can, then check again.",
  "   Stop when the check ends with Status: OK, or only with NOTEs you cannot fix.",
  "5. Try the functions once with run_r: source('<name>/R/<name>.R') and call each function.",
  "   Do not install the package into the user's library.",
  "6. Report: the files you wrote, the final check status, the path of the .tar.gz file,",
  "   and anything you could not fix.",
  "Rules: never guess what a command printed; read the tool result. Keep the functions short and correct.",
  "Do not write files outside the package folder.")

# ---- the model: the first one that is configured ----
chat <- if (nzchar(Sys.getenv("OPENAI_API_KEY"))) {
  chat_openai(system_prompt = instructions)
} else if (nzchar(Sys.getenv("ANTHROPIC_API_KEY"))) {
  chat_anthropic(system_prompt = instructions)
} else if (nzchar(Sys.getenv("COURSE_MODEL_URL"))) {
  chat_openai_compatible(base_url = Sys.getenv("COURSE_MODEL_URL"), model = Sys.getenv("COURSE_MODEL"),
                         api_key = Sys.getenv("COURSE_MODEL_KEY", "none"), system_prompt = instructions)
} else {
  message("No key found. Using Ollama llama3.2:1b, which is too small for this task; expect it to fail.")
  chat_ollama(model = "llama3.2:1b", system_prompt = instructions)
}
cat("Model:", chat$get_model(), "\nSandbox:", work, "\n")
chat$register_tools(list(tool_write, tool_read, tool_list, tool_run))

# ---- the receipt: every request and every result, as they happen ----
short <- function(x, n = 300) {                  # the first and the last n characters; the full text is in the saved record
  x <- paste(x, collapse = " ")
  if (nchar(x) > 2 * n) paste0(substr(x, 1, n), " [...] ", substr(x, nchar(x) - n + 1, nchar(x))) else x
}
chat$on_tool_request(function(request) {
  a <- request@arguments
  shown <- if (request@name == "write_file") a$path else if (request@name == "run_r") short(a$code, 120) else deparse1(a)
  cat("\n->", request@name, ":", shown, "\n")
})
chat$on_tool_result(function(result) {
  cat("<-", short(result@value), "\n")
})

# ---- one task. ellmer runs the loop: ask, act, observe, repeat, until the model answers ----
chat$chat(paste("Build this package:", idea))

# ---- what to hand in ----
cat("\nFiles in the sandbox:\n", list_files(), "\n")
chat$get_tokens()                                 # cost = tokens times the price
record <- list(
  date          = Sys.Date(),
  model         = chat$get_model(),
  system_prompt = chat$get_system_prompt(),
  tools         = chat$get_tools(),              # the tool definitions
  turns         = chat$get_turns(),              # the full transcript
  tokens        = chat$get_tokens())
saveRDS(record, file.path(work, paste0("pkg_agent_run_", Sys.Date(), ".rds")))   # the receipt, on disk
