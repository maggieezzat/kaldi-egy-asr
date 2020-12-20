with open('data/local/lm/big-lm-data/lm_train__words_list.txt', 'r') as f:
  with open('data/local/dict_big_lm/lexicon.txt', 'w') as lex:
    with open('data/local/dict_big_lm/lexiconp.txt', 'w') as lexp:
      lex.write("<UNK> SIL" + '\n')
      lexp.write("<UNK> 1.0 SIL" + '\n')
      for line in f:
        word = line.strip()
        if "<" in word or not word.isalpha():
          print(word)
        else:
          chars =  list(word)
          lex.write(word + " " + " ".join(chars) + '\n')
          lexp.write(word + " 1.0 " + " ".join(chars) + '\n')

