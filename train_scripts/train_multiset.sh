source activate dpr
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export basepath=$(pwd)

NUM_GPU=8

# Randomly set a port number
# If you encounter "address already used" error, just run again or manually set an available port id.
PORT_ID=$(expr $RANDOM + 1000)

# Allow multiple threads
export OMP_NUM_THREADS=8

python -m torch.distributed.launch --nproc_per_node=8 --master_port $PORT_ID train_dense_encoder.py \
  train_datasets=[squad1_train,trivia_train,nq_train] \
  dev_datasets=[squad1_dev] \
  train=biencoder_nq \
  output_dir=$basepath/DCSR_multiset/multiset_checkpoints
