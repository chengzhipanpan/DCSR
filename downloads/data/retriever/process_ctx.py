"""
A simple version of spliting sentence and labeling sentences with answers.

There are also some conditions that we didn't consider, which might lead to some noise in the DCSR model. We leave it for future work
"""
from tqdm import tqdm
import json

def process_paragraph(para_dict, question, answers, indicator):
    # process a paragraph and split them by sentences.
    # The paragraph instance is a dict
    text = para_dict["text"]
    
    # split text by words. first uses space as the discriminator of sentences. 
    text_words = str.split(text)
    
    new_sent_list = [["<sent>"]]
    for word_id, word in enumerate(text_words):
        if word[-1] in [".", "!", "?"]:
            abbr_flag = False
            up_case = 0

            # Abbreviation - v1
            for letter in word[:-1]:
                if not ( 'A'<=letter<='Z' or 'a'<=letter<='z' ):
                    abbr_flag = True
                if 'A'<=letter<='Z':
                    up_case += 1
            if up_case > 1:
                abbr_flag = True
            
            # Abbreviation - v2
            if len(word[:-1]) == 1 and up_case == 1:
                abbr_flag = True
            
            # --- Case 2, maybe the word is a special pharse, like etc. 
            if word in ["etc.", "e.g.", "diff.", "vs.", "i.e.", "Mr.", "Miss.", "Mrs.", "B.C.", "A.D."]:
                # print("Version 1")
                new_sent_list[-1].append(word)
            
            elif abbr_flag:
                # print("Version 2")
                new_sent_list[-1].append(word)
#             elif not dic.check(word[:-1]):
#                 new_sent_list[-1].append(word)
            
            # --- Float Number --- 
            elif word_id < len(text_words)-1 and not ('A' <= text_words[word_id+1][0] <= 'Z'):
                # The next sentence does not begin with a big letter,
                # print("Version 3")
                new_sent_list[-1].append(word)
            
            else:
                # Not the last word
                # print("Version 4")
                new_sent_list[-1].append(word)
                # if the new_sent_list[-1] only has one word, it probabily has some error
                # Probably it is a word of previous sent. but also probably the next sent.
                # Still there might be some error, but a lot better now.
                # 
                if len(new_sent_list[-1]) > 8 and word_id != len(text_words) - 1:
                    new_sent_list.append(["<sent>"])
        else:
             new_sent_list[-1].append(word)
    
    new_sent_list = [" ".join(i) for i in new_sent_list]
    
    # Now we should decide, whether each sentence is gold
    if indicator == 1:
        # This means is a positive context, and now we should check overlap.
        labels = []
        for sent in new_sent_list:
            # check whether this "sent" has some overlap with question and answer
            gold_flag = False
            
            # TODO: modify this sentence labelling logic to elliminate the potential noises.
            for ans in answers:
                if (sent.lower()).find(ans.lower()) >= 0:
                    gold_flag = True
            if gold_flag:
                labels.append(1)
            else:
                labels.append(0)
    else:
        labels = [0] * len(new_sent_list)
    
    new_sent = " ".join(new_sent_list)
    
    new_para_dict = {}
    for key in para_dict.keys():
        if key != "text":
            new_para_dict[key] = para_dict[key]
    new_para_dict["new_text"] = new_sent
    # new_para_dict["sents"] = new_sent_list
    new_para_dict["sent_labels"] = labels
    
    return new_para_dict

def process_all_samples(samples):
    new_samples = []
    for sample in tqdm(samples):
        new_sample = {}
        for key in sample.keys():
            if key not in ["positive_ctxs", "negative_ctxs", "hard_negative_ctxs", "question"]:
                new_sample[key] = sample[key]
        new_sample["positive_ctxs"] = []
        for passage in sample["positive_ctxs"][:1]:
            new_pass = process_paragraph(passage,sample["question"], sample["answers"], 1)
            new_sample["positive_ctxs"].append(new_pass)
        new_sample["hard_negative_ctxs"] = []
        for passage in sample["hard_negative_ctxs"]:
            new_pass = process_paragraph(passage,sample["question"], sample["answers"], 0)
            new_sample["hard_negative_ctxs"].append(new_pass)
        new_sample["negative_ctxs"] = []
        if len(new_sample["hard_negative_ctxs"]) == 0:
            for passage in sample["negative_ctxs"]:
                new_pass = process_paragraph(passage,sample["question"], sample["answers"], 0)
                new_sample["negative_ctxs"].append(new_pass)
        new_sample["question"] = "<sent> " + sample["question"]
        if len(new_sample["negative_ctxs"]) + len(new_sample["hard_negative_ctxs"]) > 0 and len( new_sample["positive_ctxs"]) > 0:
            new_samples.append(new_sample)
    return new_samples

# with open("./biencoder-nq-adv-hn-train.json", "r") as f:
#     input_data = json.load(f)
# new_samples = process_all_samples(input_data)
# with open("./nq-adv-hn-train.json", "w") as f:
#     json.dump(new_samples, f)

# Process trivia dataset
with open("./biencoder-trivia-dev.json", "r") as f:
    input_data = json.load(f)
new_samples = process_all_samples(input_data)
with open("./trivia-dev.json", "w") as f:
    json.dump(new_samples, f)

with open("./biencoder-trivia-train.json", "r") as f:
    input_data = json.load(f)
new_samples = process_all_samples(input_data)
with open("./trivia-train.json", "w") as f:
    json.dump(new_samples, f)

# Process NQ dataset
with open("./biencoder-nq-dev.json", "r") as f:
    input_data = json.load(f)
new_samples = process_all_samples(input_data)
with open("./nq-dev.json", "w") as f:
    json.dump(new_samples, f)

with open("./biencoder-nq-train.json", "r") as f:
    input_data = json.load(f)
new_samples = process_all_samples(input_data)
with open("./nq-train.json", "w") as f:
    json.dump(new_samples, f)

# Process squad1 dataset
with open("./biencoder-squad1-dev.json", "r") as f:
    input_data = json.load(f)
new_samples = process_all_samples(input_data)
with open("./squad1-dev.json", "w") as f:
    json.dump(new_samples, f)

with open("./biencoder-squad1-train.json", "r") as f:
    input_data = json.load(f)
new_samples = process_all_samples(input_data)
with open("./squad1-train.json", "w") as f:
    json.dump(new_samples, f)
