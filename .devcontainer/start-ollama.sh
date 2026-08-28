#!/usr/bin/env bash
# Start the Ollama server if it is not already running. Runs every time the codespace starts or VS Code attaches.
# setsid + disown: the codespace lifecycle hook kills its own background children when it exits; this survives.
if command -v ollama > /dev/null && ! pgrep -x ollama > /dev/null; then
  setsid nohup ollama serve > /tmp/ollama.log 2>&1 < /dev/null &
  disown
  for i in $(seq 1 20); do curl -s http://localhost:11434 > /dev/null && break; sleep 1; done
fi
