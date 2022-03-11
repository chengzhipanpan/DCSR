source activate dpr

export basepath=$(pwd)

cd downloads/data/retriever/

# Downloading data from source and unzip them.
wget https://dl.fbaipublicfiles.com/dpr/data/retriever/biencoder-nq-train.json.gz
gunzip biencoder-nq-train.json.gz

wget https://dl.fbaipublicfiles.com/dpr/data/retriever/biencoder-nq-dev.json.gz
gunzip biencoder-nq-dev.json.gz

wget https://dl.fbaipublicfiles.com/dpr/data/retriever/biencoder-trivia-train.json.gz
gunzip biencoder-trivia-train.json.gz

wget https://dl.fbaipublicfiles.com/dpr/data/retriever/biencoder-trivia-dev.json.gz
gunzip biencoder-trivia-dev.json.gz

wget https://dl.fbaipublicfiles.com/dpr/data/retriever/biencoder-squad1-train.json.gz
gunzip biencoder-squad1-train.json.gz

wget https://dl.fbaipublicfiles.com/dpr/data/retriever/biencoder-squad1-dev.json.gz
gunzip biencoder-squad1-dev.json.gz


# Process All Data
python process_ctx.py
