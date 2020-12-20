import os

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################

if os.path.isfile('data/local/lm/lm_train__msa_plus_transcipts.txt'):
    print("Not merging lm corpus and transcripts since merged file already exists")
else:
    #append train transcripts to lm train and append transcripts vocab to words list
    with open('data/train/text', 'r') as train_text:
        with open('data/local/lm/lm_train__msa_corpus_clean_ASMO.txt', 'r') as lm_train:
            
            with open('data/local/lm/lm_train__msa_plus_transcipts.txt', 'w') as out:
                with open('data/local/lm/lm_train__words_list.txt', 'a') as words_list:
                    for line in train_text:
                        txt = line.split(" ", 1)[1].strip()
                        txt = txt.replace("SIL", '')
                        out.write(txt + '\n')
                        words = txt.split()
                        for word in words:
                            words_list.write(word + '\n')
                    for line in lm_train:
                        out.write(line)

