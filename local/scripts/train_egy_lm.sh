#!/usr/bin/env bash

srilm_dir="../../tools/srilm/bin/i686-m64"


lm_text="data/local/lm/lm_corpus_train.txt"
lm_vocab="data/local/lm/lm_corpus_test.txt"
lm_test="data/local/lm/lm_corpus_word_list_asmo.txt"
tri_dir="data/local/lm/trigram"

lang_test_dir="data/lang_test"
dict_dir_nosp="data/local/dict_nosp"
#####################################################################



mkdir -p $tri_dir

################################################# Data Preparation ##################################################
#append train transcripts to lm train data and generate words list
#python local/scripts/gen_lm_data.py

#sort unique the words list to avoid any duplicates
sort -u -o $lm_vocab $lm_vocab 
#####################################################################################################################


################################################### LM Training #####################################################
#trigram language model with limiting bi-gram and tri-gram counts
echo "$0: Training trigram language model"
#$srilm_dir/ngram-count -text $lm_text -order 3 -limit-vocab -vocab $lm_vocab -unk -map-unk "<UNK>" -kndiscount -interpolate -lm $tri_dir/tri_lm.o3g.kn.gz -gt2min 3 -gt3min 2
$srilm_dir/ngram-count -text $lm_text -order 3 -limit-vocab -vocab $lm_vocab -unk -map-unk "<UNK>" -kndiscount -interpolate -lm $tri_dir/tri_lm.o3g.kn.gz


#measure perplexity
echo "$0: Measuring perplexity for trigram language model"
$srilm_dir/ngram -unk -lm $tri_dir/tri_lm.o3g.kn.gz -ppl $lm_test -debug 0 >& $tri_dir/tri_lm.ppl0


#convert ARPA-format language models to FSTs.
echo  "$0: Converting language model to G.fst"
utils/format_lm.sh data/lang $tri_dir/tri_lm.o3g.kn.gz $dict_dir_nosp/lexicon.txt $lang_test_dir
#####################################################################################################################