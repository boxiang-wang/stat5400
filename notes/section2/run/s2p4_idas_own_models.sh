# Run with:  source ~/classFiles/notes/section2/run/s2p4_idas_own_models.sh
#            (not "bash ...": then "ollama" is not found afterwards)
# Route 2: download Ollama and one model into your home folder.
# Downloads 1.4 GB (program) + 3.4 GB (model) and uses about 6 GB of disk. Takes a few minutes.

# 1. Make the folder ~/ollama, then download the Ollama program (a .tar.zst file, 1.4 GB)
mkdir -p $HOME/ollama && curl -L https://ollama.com/download/ollama-linux-amd64.tar.zst -o $HOME/ollama.tar.zst
# 2. Unpack it into ~/ollama (IDAS has no zstd program, so the class copy of the Python package pyzstd unpacks it)
PYTHONPATH=$HOME/classdata/models/python python -m pyzstd -d $HOME/ollama.tar.zst --tar-output-dir $HOME/ollama
# 3. Let the shell find ollama, and keep your models in ~/ollama-models
export PATH=$HOME/ollama/bin:$PATH OLLAMA_MODELS=$HOME/ollama-models
# 4. Start Ollama in the background (messages go to ~/ollama.log), then wait 5 seconds
nohup ollama serve > $HOME/ollama.log 2>&1 & sleep 5
# 5. Download one model (3.4 GB)
ollama pull qwen3.5:4b
# 6. Make the model use 8 threads, the CPUs your IDAS session has (the default is much slower)
printf 'FROM qwen3.5:4b\nPARAMETER num_thread 8\n' | ollama create qwen3.5:4b -f /dev/stdin
