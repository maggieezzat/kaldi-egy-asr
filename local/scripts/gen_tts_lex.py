import os

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################

if not os.path.exists('data/local/dict_tts'):
    os.makedirs('data/local/dict_tts')


all_vocab = {}

with open('data/local/dict_tts/lexicon.txt', 'w') as out:
    with open('data/local/dict_tts/lexiconp.txt', 'w') as out_p:
        
        with open('data/local/dict/lexicon.txt', 'r') as f:
            print("Processing standard lexicon..")
            i = 0
            for line in f:
                i+=1
                print("Processing line: " + str(i), end='\r')
                line = line.strip().split(" ", 1)
                word = line[0].strip()
                lex_ = line[1].strip()
                lex = lex_.replace(' ', '')
                if word == lex or word == '<UNK>':
                    if word not in all_vocab.keys():
                        out.write(word + "    " + lex_ + '\n')
                        out_p.write(word + "    1.0    " + lex_ + '\n')
                        all_vocab[word] = word
        
        with open('tts/tts_lm_words.txt', 'r') as f:
            print("Processing lm words list..")
            i = 0
            for line in f:
                i+=1
                print("Processing line: " + str(i), end='\r')
                if (line.strip() not in all_vocab):
                    print("not in vocab")
                    lex = " ".join(line.strip())
                    out.write(line.strip() + "    " + lex + '\n')
                    out_p.write(line.strip() + "    1.0    " + lex + '\n')
                    all_vocab[line.strip()] = line.strip()
        


