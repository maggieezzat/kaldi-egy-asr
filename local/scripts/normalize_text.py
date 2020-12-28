import os


def get_dict(in_files=['data/train_coll/text_ar_2', 'data/coll_dev_10/text_ar'], out_file='data/train_coll/dict.txt', out_no_counts='data/train_coll/dict_no_counts.txt'):
    unique_words = {}

    for in_file in in_files:
        with open(in_file, 'r') as f:
            for line in f:
                line = line.strip().split(" ", 1)
                line = line[1]
                words = line.split()
                for word in words:
                    if word in unique_words:
                        unique_words[word] +=1
                    else:
                        unique_words[word] = 1
    sorted_words = sorted(unique_words.items(), key=lambda x: x[1], reverse=True)
    
    with open(out_file, 'w') as out:
        with open(out_no_counts, 'w') as out2:
            for item in sorted_words:
                out.write(item[0] + " " + str(item[1]) + '\n') 
                out2.write(item[0] + '\n')



def get_pairs(out_file, char1, char2, in_file='data/train_coll/dict.txt'):

    char1_words = {}
    char2_words = {}

    with open(in_file, 'r') as f:
        for line in f:
            line = line.strip().split()
            word_ = line[0]
            count_ = line[1]
            if char1 in word_:
                char1_words[word_] = count_
            elif char2 in word_:
                char2_words[word_] = count_
    out_file_1 = out_file + "-MORE-" + char1 + ".txt"
    out_file_2 = out_file + "-MORE-" + char2 + ".txt"
    
    with open(out_file_1, 'w') as out1:
        with open(out_file_2, 'w') as out2:
            for word, count in char1_words.items():
                repl = word.replace(char1, char2)
                if repl in char2_words.keys():
                    repl_count = char2_words[repl]
                    if int(count) > int(repl_count) and (int(repl_count)<100 or (int(count)-int(repl_count))>100 ):
                        out1.write(word + " " + count + "   " + repl + " " + repl_count + '\n')
                    else:
                        out2.write(word + " " + count + "   " + repl + " " + repl_count + '\n')



def apply_cleaning(pairs_list, correct_char, in_text, out_text):

    mapping = {}

    with open(pairs_list, 'r') as f:
        for line in f:
            line = line.strip().split()
            w1 = line[0]
            w2 = line[2]
            if correct_char in w1:
                mapping[w2] = w1
            else:
                mapping[w1] = w2
    
    with open(in_text, 'r') as f:
        with open(out_text, 'w') as out:
            for line in f:
                for key, val in mapping.items():
                    line = line.replace(key, val)
                out.write(line)



def main():
    pass



if __name__ == "__main__":
    main()