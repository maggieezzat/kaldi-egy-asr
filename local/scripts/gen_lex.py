import os

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-EGY-ASR)
#############################################################################



def create_normal_lex(lex_path, text_path, lm_words_path):

    words = []
    with open(text_path, 'r') as f:
        for line in f:
            line = line.strip().split(" ", 1)
            if len(line) >1:
                text = line[1]
                tokens = text.split()
                for token in tokens:
                    words.append(token)
    
    with open(lm_words_path, 'r') as f:
        for line in f:
            line = line.strip()
            words.append(line)
    
    words = list(set(words))

    with open(lex_path, 'w') as out:
        out.write("<UNK> SIL\n")
        for word in words:
            if '<' or '>' in word:
              continue
            out.write(word + " " + " ".join(list(word)) + '\n')




def create_coll_lex(lex_path, text_path, lm_words_path):
    pass




def main():
    lex_dir = 'data/local/dict_nosp'
    if not os.path.exists(lex_dir):
        os.makedirs(lex_dir)
    create_normal_lex(lex_path=lex_dir+'/lexicon.txt', text_path='data/train_coll/text', lm_words_path='data/local/lm/lm_corpus_word_list_asmo.txt')


if __name__ == "__main__":
    main()

