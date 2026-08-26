#!/usr/bin/env bash
# Install Ollama and pull the two small course models. Runs once when the codespace is built.
set -x
command -v zstd > /dev/null || (sudo apt-get update && sudo apt-get install -y zstd)
curl -fsSL https://ollama.com/install.sh | sh
nohup ollama serve > /tmp/ollama.log 2>&1 &
for i in $(seq 1 60); do curl -s http://localhost:11434 > /dev/null && break; sleep 1; done
ollama pull qwen2.5:0.5b
ollama pull llama3.2:1b
ollama list
