import os

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-EGY-ASR)
#############################################################################



def create_normal_lex(lex_path, lexp_path, text_path, lm_words_path):

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
    print(len(words))

    with open(lex_path, 'w') as lex:
        with open(lexp_path, 'w') as lexp:
            lex.write("<UNK> SIL\n")
            lex.flush()
            lexp.write("<UNK> 1.0 SIL\n")
            lexp.flush()
            for word in words:
                if word == '<UNK>':
                    continue
                lex.write(word + " " + " ".join(list(word)) + '\n')
                lex.flush()
                lexp.write(word + " 1.0 " + " ".join(list(word)) + '\n')
                lexp.flush()



def coda_rules(word):

    coll_words = []
    coll_words.append(word)
    
    #ق -> ء 
    if 'b' in word:
        coll_words.append(word.replace('b', 'A'))
    #ث -> ط س ت 
    if 'K' in word:
        coll_words.append(word.replace('K', 'W'))
        coll_words.append(word.replace('K', 'S'))
        coll_words.append(word.replace('K', 'J'))
    #ذ -> د ز
    if 'P' in word:
        coll_words.append(word.replace('P', 'O'))
        coll_words.append(word.replace('P', 'R'))
    #ض > ظ ز د
    if 'V' in word:
        coll_words.append(word.replace('V', 'X'))
        coll_words.append(word.replace('V', 'R'))
        coll_words.append(word.replace('V', 'O'))
    #ظ -> ض ز ذ
    if 'X' in word:
        coll_words.append(word.replace('X', 'V'))
        coll_words.append(word.replace('X', 'R'))
        coll_words.append(word.replace('X', 'P'))
    #ص -> س ص
    if 'U' in word:
        coll_words.append(word.replace('U', 'S'))
    #ط -> ت ط
    if 'W' in word:
        coll_words.append(word.replace('W', 'J'))

    return coll_words




def create_coll_lex(lex_path, lexp_path, text_path, lm_words_path):
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
    print(len(words))

    with open(lex_path, 'w') as lex:
        with open(lexp_path, 'w') as lexp:
            lex.write("<UNK> SIL\n")
            lex.flush()
            lexp.write("<UNK> 1.0 SIL\n")
            lexp.flush()
            for word in words:
                if word == '<UNK>':
                    continue
                
                coll_words = coda_rules(word)
                prob = 1.0/len(coll_words)
                prob_str = "{:.2f}".format(prob)
                for coll_word in coll_words:
                    lex.write(coll_word + " " + " ".join(list(coll_word)) + '\n')
                    lex.flush()
                    lexp.write(coll_word + " " + prob_str + " " + " ".join(list(coll_word)) + '\n')
                    lexp.flush()




def main():

    '''
    lex_dir = 'data/local/dict_nosp'
    if not os.path.exists(lex_dir):
        os.makedirs(lex_dir)
    lex_file = lex_dir + '/lexicon.txt'
    lexp_file = lex_dir + '/lexiconp.txt'
    create_normal_lex(lex_path=lex_file, lexp_path=lexp_file, text_path='data/train/text', lm_words_path='data/local/lm/lm_corpus_word_list_asmo.txt')
    '''
    ############################################# COLLIQUAL LEX #############################################
    lex_dir = 'data/local/dict_nosp_coll'
    if not os.path.exists(lex_dir):
        os.makedirs(lex_dir)
    lex_file = lex_dir + '/lexicon.txt'
    lexp_file = lex_dir + '/lexiconp.txt'
    create_coll_lex(lex_path=lex_file, lexp_path=lexp_file, text_path='data/train_coll/text', lm_words_path='data/local/lm_coll/lm_corpus_word_list_asmo.txt')
    

if __name__ == "__main__":
    main()

