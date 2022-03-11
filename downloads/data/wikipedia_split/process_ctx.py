"""
Preparing sentence-aware wikipedia corpus.
"""
import pandas as pd
from tqdm import tqdm
data = pd.read_csv("./psgs_w100.tsv", sep="\t")
# print(data.info())

def process_paragraph_v2(context):
    text = context
    
    # split text by words. first uses space as the discriminator of sentences. 
    text_words = str.split(text)
    
    new_sent_list = [["<sent>"]]
    for word_id, word in enumerate(text_words):
        if word[-1] in [".", "!", "?"]:
            # print("Checking word...", word)
            # Possibly, end of a sentence.
            
            # --- Case 1, the word starts with a big letter, meaning that its a Mr. or Mrs. or Name or Something. then its not a sentence.
            abbr_flag = False
            up_case = 0
            for letter in word[:-1]:
                if not ( 'A'<=letter<='Z' or 'a'<=letter<='z' ):
                    abbr_flag = True
                if 'A'<=letter<='Z':
                    up_case += 1
            if up_case > 1:
                abbr_flag = True
            
            if len(word[:-1]) == 1 and up_case == 1:
                abbr_flag = True
            
            # --- Case 2, maybe the word is a special pharse, like etc. 
            if word in ["etc.", "e.g.", "diff.", "vs.", "i.e.", "Mr.", "Miss.", "Mrs.", "B.C.", "A.D."]:
                # print("Version 1")
                new_sent_list[-1].append(word)
            
            elif abbr_flag:
                # print("Version 2")
                new_sent_list[-1].append(word)
  
            # --- Case 3, it might be a float number. Then probably, the next is also a number. Should not be a sentence beginner. 
            elif word_id < len(text_words)-1 and not ('A' <= text_words[word_id+1][0] <= 'Z'):
                # The next sentence does not begin with a big letter,
                # print("Version 3")
                new_sent_list[-1].append(word)
            
            else:
                new_sent_list[-1].append(word)
                if len(new_sent_list[-1]) > 8 and word_id != len(text_words) - 1:
                    new_sent_list.append(["<sent>"])
        else:
             new_sent_list[-1].append(word)
    
    if len(new_sent_list[-1]) < 8:
        new_sent_list[-1] = new_sent_list[-1][1:]
    new_sent_list = [" ".join(i) for i in new_sent_list]
    
    new_sent = " ".join(new_sent_list)
    
    return new_sent.count("<sent>"), new_sent

ids = data["id"].values
texts = data["text"].values
titles = data["title"].values

new_text = []
sent_len = []
for ctx in tqdm(texts):
    length, new_ctx = process_paragraph_v2(ctx)
    new_text.append(new_ctx)
    sent_len.append(length)

print("Average Length of the whole corpus: ", sum(sent_len) / len(sent_len))
data_to_save = {"id": ids, "text":new_text, "title":titles}
data_to_save = pd.DataFrame(data_to_save)
data_to_save.to_csv("./psgs_w100.tsv", sep="\t", index=None)
