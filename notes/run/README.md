# Run-in-Codespace files

Each file here is a code block from the lecture notes that needs a real R
(a C++ compiler or a precise clock), so it cannot run inside the web page.

Open the file, put the cursor on a line and press Ctrl+Enter (Cmd+Enter on Mac)
to run it in the R console, or select all and run.

- `s1p1_microbenchmark.R` — Section 1.1, timing sqrt(x) vs x^0.5 with microbenchmark
- `s1p1_sumC.R` — Section 1.1, an R loop vs C++ (Rcpp) vs the built-in sum()
- `s1p1_llm.R`, `s1p1_llm.py` — Section 1.1, first LLM API call (needs the GEMINI_API_KEY Codespaces secret)
- `s1p1_ollama.R` — Section 1.1, two local models (qwen2.5:0.5b, llama3.2:1b) through Ollama; no key needed
