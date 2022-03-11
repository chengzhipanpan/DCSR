import os
import sys
import time

def generate_shard(shard_id, shard_num, mpath, opath):
    os.system("echo %d" % shard_id)
    os.system("""python3 generate_dense_embeddings_allsents.py \
                        model_file=%s \
                        ctx_src=dpr_wiki \
                        shard_id=%d num_shards=%d \
                        out_file=%s/wiki_passages""" % (mpath, shard_id, shard_num, opath))

m_path = sys.argv[1]
o_path = sys.argv[2]
shard_num = int(sys.argv[3])
max_shard_num = int(sys.argv[4])

for i in range(max_shard_num):
    try:
        cur_files = os.listdir(o_path)
    except:
        cur_files = []
        os.makedirs(o_path)
    has_flag = False
    for f in cur_files:
        number_cur_f = int(str.split(f, sep="_")[-1])
        if number_cur_f == i:
            has_flag = True
    while not has_flag:
        generate_shard(i, shard_num, m_path, o_path)
        cur_files = os.listdir(o_path)
        for f in cur_files:
            number_cur_f = int(str.split(f, sep="_")[-1])
            if number_cur_f == i:
                has_flag = True
        time.sleep(10)
