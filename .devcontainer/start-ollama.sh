#!/usr/bin/env bash
# Start the Ollama server if it is not already running. Runs every time the codespace starts.
if command -v ollama > /dev/null && ! pgrep -x ollama > /dev/null; then
  nohup ollama serve > /tmp/ollama.log 2>&1 &
fi
