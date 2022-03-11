source activate dpr

export basepath=$(pwd)

cd downloads/data/wikipedia_split/

# Downloading data from source and unzip them.
wget https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz
gunzip psgs_w100.tsv.gz

# Process All Data
python process_ctx.py
