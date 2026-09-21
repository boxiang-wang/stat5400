# Run with:  source ~/classFiles/notes/section2/run/s2p4_idas_models.sh
#            (not "bash ...": then "ollama" is not found afterwards)
# Route 1: use the Ollama program and the models in classdata. Nothing is downloaded.

# 1. Let the shell find the ollama program in classdata
export PATH=$HOME/classdata/models/ollama/bin:$PATH
# 2. Tell Ollama where the class models are
export OLLAMA_MODELS=$HOME/classdata/models/library
# 3. Tell Ollama not to clean up that folder (it is read-only for students)
export OLLAMA_NOPRUNE=1
# 4. Start Ollama in the background, unless it is already running; its messages go to ~/ollama.log
pgrep -x ollama > /dev/null || nohup ollama serve > $HOME/ollama.log 2>&1 &
# 5. Wait 5 seconds for it to start
sleep 5
# 6. List the models you can use
ollama list
