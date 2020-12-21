import re
from arabic_asmo_converter import conv_asmo



def clean_lm(corpus_path, out_path):
    i=0
    with open(corpus_path, 'r') as f:
        with open(out_path, 'w') as out:
            for line in f:
                i+=1
                if i%500000 == 0:
                    print("Line: " + str(i), end='\r')
                if '<unk>' in line or '<num>' in line or '<url>' in line:
                    continue
                else:
                    line = line.replace('.', '')
                    line = line.replace('?', '')
                    line = line.replace('؟', '')
                    line = re.sub(' +', ' ', line)
                    line = line.strip()
                    if len(line.split())>1:
                        out.write(line + '\n')



def gen_words_list(dict_path, out_path, threshold=4):

    with open(dict_path, 'r') as f:
        with open(out_path, 'w') as out:
            for line in f:
                if '<unk>' in line or '<num>' in line or '<url>' in line or '.' in line or '?' in line or '؟' in line:
                    continue
                else:
                    word = line.strip().split()[0]
                    count = line.strip().split()[1]
                    if int(count) <= threshold:
                        break
                    out.write(word + '\n')



def convert_word_list(word_list, out_path):
    with open(word_list, 'r') as f:
        with open(out_path, 'w') as out:
            for line in f:
                line = line.strip()
                asmo_line = conv_asmo(line)
                out.write(asmo_line + '\n')



def split_train_test(lm_corpus_asmo, train_lm, test_lm):

    i=0
    test_words = {}
    with open(lm_corpus_asmo, 'r') as f:
        with open(train_lm, 'w') as train:
            with open(test_lm, 'w') as test:
                for line in f:
                    i+=1
                    if i%100000 == 0 and len(test_words)<150000:
                        test.write(line)
                        words = line.strip().split()
                        for word in words:
                            test_words[word] = word
                    else:
                        train.write(line)




def main():
    
    clean_lm(corpus_path='local/data/lang_model/corpus_merged_clean_3.txt', out_path='local/data/lang_model/lm_corpus_clean.txt')
    gen_words_list(dict_path='local/data/lang_model/corpus_merged_final_dict.txt', out_path='local/data/lang_model/lm_corpus_word_list.txt')
    convert_word_list(word_list='local/data/lang_model/lm_corpus_word_list.txt', out_path='local/data/lang_model/lm_corpus_word_list_asmo.txt')

    split_train_test(lm_corpus_asmo='local/data/lang_model/lm_corpus_clean_asmo.txt', 
        train_lm='data/local/lm/lm_corpus_train.txt', test_lm='data/local/lm/lm_corpus_test.txt')


if __name__ == "__main__":
    main()
