export model_path=/path/to/your/model
export out_dir=/path/to/save/embedding
export shard_num=40
export max_shard=40
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

python train_scripts/generate_shard.py $model_path $out_dir $shard_num $max_shard

python dense_retriever.py \
	model_file=$model_path \
	qa_dataset=squad1_test \
	ctx_datatsets=[dpr_wiki] \
	encoded_ctx_files=[\"$out_dir/wiki_passages_*\"] \
	out_file=./output_result/squad_result.json

python dense_retriever.py \
	model_file=$model_path \
	qa_dataset=trivia_test \
	ctx_datatsets=[dpr_wiki] \
	encoded_ctx_files=[\"$out_dir/wiki_passages_*\"] \
	out_file=./output_result/trivia_result.json

python dense_retriever.py \
	model_file=$model_path \
	qa_dataset=nq_test \
	ctx_datatsets=[dpr_wiki] \
	encoded_ctx_files=[\"$out_dir/wiki_passages_*\"] \
	out_file=./output_result/nq_result.json