import os

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################

if os.path.isfile('data/local/lm/lm_train__vocab.txt'):
    print("Not creating language model vocab file since it already exists")
else:
    #generate vocab file with counts
    vocab = {}
    i=0
    with open('data/local/lm/lm_train__msa_corpus_clean_ASMO.txt', 'r') as lm_train:
        for line in lm_train:
            i+=1
            print("Processing Line: " + str(i), end='\r')
            words = line.strip().split(" ")
            for word in words:
                if vocab.get(word) == None:    
                    vocab[word] = 1
                else:
                    vocab[word] += 1

    sorted_vocab = []
    for k,v in vocab.items():
        sorted_vocab.append((k,v))

    sorted_vocab = sorted(sorted_vocab, key=lambda x: x[1], reverse=True)

    with open('data/local/lm/lm_train__vocab.txt', 'w', encoding='utf-8') as f:
        for item in sorted_vocab:
            f.write(item[0] + " " + str(item[1]) + "\n")