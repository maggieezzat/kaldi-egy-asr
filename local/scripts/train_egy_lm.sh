#!/usr/bin/env bash

srilm_dir="../../tools/srilm/bin/i686-m64"

lm_type=""
#lm_type="_coll"

bi_min=8
tri_min=5

#####################################################################

lm_text="data/local/lm$lm_type/lm_corpus_train.txt"

lm_vocab="data/local/lm$lm_type/lm_corpus_word_list_asmo.txt"

lm_test="data/local/lm$lm_type/lm_corpus_test.txt"

tri_dir="data/local/lm$lm_type/trigram"

lang_test_dir="data/lang_test$lm_type"

dict_dir_nosp="data/local/dict_nosp$lm_type"
#####################################################################


mkdir -p $tri_dir

################################################### LM Training #####################################################
#trigram language model with limiting bi-gram and tri-gram counts
echo "$0: Training trigram language model"
$srilm_dir/ngram-count -text $lm_text -order 3 -limit-vocab -vocab $lm_vocab -unk -map-unk "<UNK>" -kndiscount -interpolate -lm $tri_dir/tri_lm.o3g.kn.gz -gt2min $bi_min -gt3min $tri_min


#measure perplexity
echo "$0: Measuring perplexity for trigram language model"
$srilm_dir/ngram -unk -lm $tri_dir/tri_lm.o3g.kn.gz -ppl $lm_test -debug 0 >& $tri_dir/tri_lm.ppl0


#convert ARPA-format language models to FSTs.
echo  "$0: Converting language model to G.fst"
utils/format_lm.sh data/lang $tri_dir/tri_lm.o3g.kn.gz $dict_dir_nosp/lexicon.txt $lang_test_dir
#####################################################################################################################
