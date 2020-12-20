import os
import sys

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################

if len(sys.argv)>1:
    thresh = int(sys.argv[1])
else:
    thresh=11

if os.path.isfile('data/local/lm/lm_train__words_list.txt'):
    print("Not cutting language model vocab file nor creating words list since it already exists")
else:
    with open('data/local/lm/lm_train__vocab.txt', 'r') as f:
        with open('data/local/lm/lm_train__words_list.txt', 'w') as out:
            for line in f:
                line = line.strip().split()
                word = line[0]
                count = int(line[1])
                if count>thresh:
                    out.write(word + '\n')
                else:
                    break

