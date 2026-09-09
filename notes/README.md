# Files to run in the Codespace

Each lecture page lives in its own section folder, together with the files that
belong to it:

    notes/section1/s1p1.qmd      the page
    notes/section1/img/          figures
    notes/section1/run/          code that needs a real R (compiler, clock, API key)
    notes/section1/vibe/         starter files for the AI-assisted tasks
    notes/section1/code/         all code from the page, generated: .R .py .Rmd .ipynb

The files under `run/` are code blocks from the notes that cannot run inside the
web page. Open one, put the cursor on a line and press Ctrl+Enter (Cmd+Enter on
Mac) to run it in the R console, or select all and run.

- `section1/run/s1p1_microbenchmark.R` — Section 1.1, timing sqrt(x) vs x^0.5 with microbenchmark
- `section1/run/s1p1_sumC.R` — Section 1.1, an R loop vs C++ (Rcpp) vs the built-in sum()
- `section1/run/s1p1_llm.R`, `section1/run/s1p1_llm.py` — Section 1.1, first LLM API call (needs the GEMINI_API_KEY Codespaces secret)
- `section1/run/s1p1_ollama.R` — Section 1.1, two local models (qwen2.5:0.5b, llama3.2:1b) through Ollama; no key needed
- `section2/run/s2p3_quadratic.R` — Section 2.3, the quadratic solver as its own file (for `source()`)
- `section2/run/s2p3_quadratic.py` — Section 2.3, the same solver as a Python module (for `import`)
- `section2/run/s2p3_microbenchmark.R` — Section 2.3, timing three factorial implementations
- `section2/run/s2p3_ggplot.R` — Section 2.3, the ggplot2 example (ggplot2 is not in the browser session)
- `section2/run/s2p3_plotnine.py` — Section 2.3, the plotnine version of the same plot (plotnine is not in the browser session)
- `section3/run/s3p2_ggplot.R` - Section 3.2, one-dimensional sample means with ggplot2
- `section3/run/s3p2_binom_ci.R` - Section 3.2, six binomial confidence intervals at B = 10000 (needs the binom package)
- `section7/run/s7p1_agent_ellmer.R` - Section 7.1, the regression agent with a real model through ellmer (course model or Ollama)
- `section7/run/s7p1_agent_openai.py` - Section 7.1, the same agent loop written out against the OpenAI Responses API (any OpenAI-compatible endpoint)
- `section7/run/s7p1_agent_anthropic.py` - Section 7.1, the same loop against the Anthropic Messages API (reference; needs a key)
