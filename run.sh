#!/usr/bin/env bash

stage=0

cmd="run.pl"
nj=$(nproc)

#COLLOCIAL DATA SPLITS
train_coll_dir="data/train_coll"
train_coll_30="data/train_coll_30"
train_coll_50="data/train_coll_50"
train_coll_150="data/train_coll_150"
train_coll_250="data/train_coll_250"

#ALL DATA SPLITS (COLL+MSA)
train_dir="data/train"
train_dir_500="data/train_500"
train_dir_800="data/train_800"

#TEST SET
test_dir="data/coll_dev_10"

#LANG DIRECTORIES
lang_dir="data/lang"
lang_test_dir="data/lang_test"

#DICT DIRECTORIES
dict_dir_nosp="data/local/dict_nosp"
dict_dir="data/local/dict"

#LANGUAGE MODEL DIRECTORY
lm_dir="data/local/lm/trigram"


. ./path.sh
. ./utils/parse_options.sh

################################################## Data Preparation #################################################
if [ $stage -le 0 ]; then
    echo "############################################# Data Preparation ############################################"
    echo "$0: Creating necessary files and preparing data."

    #create wav.scp, text and utt2spk file for each of the train, dev and test set
    python3 local/scripts/gen_wavscp_uttspk_text.py

    #create utt2spk and fix data dir
    for x in $train_dir $train_coll_dir $test_dir; do
        #sort the files
        sort -u -o $x/wav.scp $x/wav.scp
        sort -u -o $x/text $x/text
        sort -u -o $x/utt2spk $x/utt2spk
        #make spk2utt file
        utils/utt2spk_to_spk2utt.pl $x/utt2spk > $x/spk2utt
        #fix data directory
        utils/fix_data_dir.sh $x
    done

fi
#####################################################################################################################



################################################## Feature Extraction ###############################################
if [ $stage -le 1 ]; then

    echo "############################################# Feature Extraction ##########################################"
    echo "$0: Extracting features"

    for x in $train_dir $train_coll_dir $test_dir; do
        #make Mel Frequency features
        log_dir="$x/log"
        mfcc_dir="$x/mfcc"
        vad_dir="$x/vad"
        segments_dir="$x/segments"
        cmvn_dir="$x/cmvn"
        steps/make_mfcc.sh --mfcc-config conf/mfcc.conf --nj $nj --cmd "$cmd" --write-utt2num-frames true $x $log_dir $mfcc_dir || exit 1;

        #fix data directory
        utils/fix_data_dir.sh $x 

        #compute cepstral mean and variance statistics per speaker.
        steps/compute_cmvn_stats.sh $x $log_dir $cmvn_dir || exit 1;

        #fix data directory
        utils/fix_data_dir.sh $x
    done

fi
#####################################################################################################################



############################################ Lexicon & Lang directory #########################################
if [ $stage -le 2 ]; then

    echo "#################################### Lexicon & Lang directory #######################################"
    echo "$0: Lexicon & Lang directory"
    #LEXICON AND LM
    python3 local/scripts/lm_scripts/clean_lm_data.py
    sort -u -o data/local/lm/lm_corpus_word_list_asmo.txt data/local/lm/lm_corpus_word_list_asmo.txt
    python3 local/scripts/gen_lex.py
    
    #create nonsilence_phones.txt, optional_silence.txt, silence_phones.txt files
    ./local/scripts/create_phones.sh $dict_dir_nosp

    #create files for data/lang
    utils/prepare_lang.sh $dict_dir_nosp "<UNK>" data/local/lang $lang_dir || exit 1;
    #create files for data/lang_test
    utils/prepare_lang.sh $dict_dir_nosp "<UNK>" data/local/lang $lang_test_dir || exit 1;

fi
#####################################################################################################################



############################################# Language Model Training ###############################################
if [ $stage -le 3 ]; then
    echo "######################################## Language Model Training ##########################################"
    ./local/scripts/train_egy_lm.sh
fi
#####################################################################################################################



################################################## Splitting Data ###################################################
if [ $stage -le 4 ]; then
    echo "############################################# Splitting Data ##############################################"
    echo "$0: Splitting Data"
    #monophone: 33.74h
    utils/subset_data_dir.sh --shortest $train_coll_dir 30000 $train_coll_30 || exit 1;

    #1st tri: 52.07h
    utils/subset_data_dir.sh $train_coll_dir 30000 $train_coll_50 || exit 1;
    #2nd tri: 156.16h
    utils/subset_data_dir.sh $train_coll_dir 90000 $train_coll_150 || exit 1;
    #3rd tri: 260.23h
    utils/subset_data_dir.sh $train_coll_dir 150000 $train_coll_250 || exit 1;

    #5th tri: 431.05h
    utils/subset_data_dir.sh $train_dir 300000 $train_dir_500 || exit 1;
    #6th tri:
    utils/subset_data_dir.sh $train_dir 500000 $train_dir_800 || exit 1;
fi
#####################################################################################################################


################################################ Monophone Training #################################################
if [ $stage -le 5 ]; then
    echo "########################################### Monophone Training ############################################"
    echo "$0: Training Monophone"

    # monophone training
    steps/train_mono.sh --nj $nj --cmd "$cmd" $train_coll_30 $lang_dir exp/mono || exit 1;
fi
#####################################################################################################################



############################################# First Triphone Training ###############################################
if [ $stage -le 6 ]; then
    echo "######################################## First Triphone Training ##########################################"
    echo "$0: FIRST triphone training"

    #aligning data in data/train_coll_50 using model from exp/mono, putting alignments in exp/mono_ali
    steps/align_si.sh --nj $nj --cmd "$cmd" $train_coll_50 $lang_dir exp/mono exp/mono_ali || exit 1;

    #train with delta features
    steps/train_deltas.sh --cmd "$cmd" 2000 10000 $train_coll_50 $lang_dir exp/mono_ali exp/tri1 || exit 1;
fi
#####################################################################################################################



############################################# Second Triphone Training ##############################################
if [ $stage -le 7 ]; then
    echo "######################################## Second Triphone Training #########################################"
    echo "$0: SECOND triphone training"

    #aligning data in data/train using model from exp/tri1, putting alignments in exp/tri1_ali
    steps/align_si.sh --nj $nj --cmd "$cmd" $train_coll_150 $lang_dir exp/tri1 exp/tri1_ali || exit 1;

    #train with delta features
    steps/train_deltas.sh --cmd "$cmd" 3000 30000 $train_coll_150 $lang_dir exp/tri1_ali exp/tri2 || exit 1;
fi
#####################################################################################################################



############################################# THIRD Triphone Training ##############################################
if [ $stage -le 8 ]; then
    echo "######################################## THIRD Triphone Training ##########################################"
    echo "$0: THIRD triphone training"

    #aligning data in data/train using model from exp/tri2, putting alignments in exp/tri2_ali
    steps/align_si.sh --nj $nj --cmd "$cmd" $train_coll_250 $lang_dir exp/tri2 exp/tri2_ali || exit 1;

    #train with delta features
    steps/train_deltas.sh --cmd "$cmd" 4000 60000 $train_coll_250 $lang_dir exp/tri2_ali exp/tri3 || exit 1;
fi
#####################################################################################################################



############################################ LDA-MLLT Triphones Training ############################################
if [ $stage -le 9 ]; then
    echo "############################################ LDA-MLLT Triphones Training ############################################"
    echo "$0: FOURTH triphone training"

    #aligning data in data/train using model from exp/tri3, putting alignments in exp/tri3_ali
    steps/align_si.sh --nj $nj --cmd "$cmd" --use-graphs true $train_coll_dir $lang_dir exp/tri3 exp/tri3_ali  || exit 1;

    #train LDA-MLLT triphones
    steps/train_lda_mllt.sh --cmd "$cmd" 7000 100000 $train_coll_dir $lang_dir exp/tri3_ali exp/tri4 || exit 1;

    #Pronunciation & Silence Probabilities
    #now we compute the pronunciation and silence probabilities from training data and re-create the lang directory.
    steps/get_prons.sh --cmd "$cmd" $train_coll_dir $lang_dir exp/tri4 || exit 1;
  
    utils/dict_dir_add_pronprobs.sh --max-normalize true $dict_dir_nosp exp/tri4/pron_counts_nowb.txt exp/tri4/sil_counts_nowb.txt exp/tri4/pron_bigram_counts_nowb.txt $dict_dir || exit 1;

    utils/prepare_lang.sh $dict_dir "<UNK>" data/local/lang $lang_dir || exit 1;
    rm $lang_test_dir/G.fst
    utils/prepare_lang.sh $dict_dir "<UNK>" data/local/lang $lang_test_dir || exit 1;

    utils/format_lm.sh data/lang $lm_dir/tri_lm.o3g.kn.gz $dict_dir/lexicon.txt $lang_test_dir || exit 1;
fi
#####################################################################################################################



############################################### SAT Triphones Training ##############################################
if [ $stage -le 10 ]; then
    echo "########################################## SAT Triphones Training #########################################"
    echo "$0: FIFTH triphone training"

    #Align LDA-MLLT triphones with FMLLR
    steps/align_fmllr.sh --nj $nj --cmd "$cmd" $train_dir_500 $lang_dir exp/tri4 exp/tri4_ali || exit 1;

    #Train SAT triphones
    steps/train_sat_basis.sh --cmd "$cmd" 10000 150000 $train_dir_500 $lang_dir exp/tri4_ali exp/tri5
    
fi
#####################################################################################################################



############################################ LDA-MLLT Triphones Training ############################################
if [ $stage -le 11 ]; then
    echo "####################################### LDA-MLLT Triphones Training #######################################"
    echo "$0: SIXTH triphone training"

    #Align SAT triphones with FMLLR
    steps/align_basis_fmllr.sh  --nj $nj --cmd "$cmd" $train_dir_800 $lang_dir exp/tri5 exp/tri5_ali

    #train second pass of LDA-MLLT
    steps/train_lda_mllt.sh --cmd "$cmd" 13000 220000 $train_dir_800 $lang_dir exp/tri5_ali exp/tri6
fi
#####################################################################################################################



############################################### SAT Triphones Training ##############################################
if [ $stage -le 12 ]; then
    echo "########################################## SAT Triphones Training #########################################"
    echo "$0: SEVENTH triphone training"

    #Align LDA-MLLT triphones with FMLLR
    steps/align_fmllr.sh --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri6 exp/tri6_ali
    
    #Train SAT triphones
    steps/train_sat_basis.sh --cmd "$cmd" 16000 300000 $train_dir $lang_dir exp/tri6_ali exp/tri7

fi
#####################################################################################################################



############################################ LDA-MLLT Triphones Training ############################################
if [ $stage -le 13 ]; then
    echo "####################################### LDA-MLLT Triphones Training #######################################"
    echo "$0: EIGTH triphone training"

    #Align SAT triphones with FMLLR
    steps/align_basis_fmllr.sh  --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri7 exp/tri7_ali

    #train third pass of LDA-MLLT
    steps/train_lda_mllt.sh --cmd "$cmd" 19000 380000 $train_dir $lang_dir exp/tri7_ali exp/tri8
fi
#####################################################################################################################



############################################### SAT Triphones Training ##############################################
if [ $stage -le 14 ]; then
    echo "########################################## SAT Triphones Training #########################################"
    echo "$0: NINTH triphone training"

    #Align LDA-MLLT triphones with FMLLR
    steps/align_fmllr.sh --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri8 exp/tri8_ali
    
    #Train SAT triphones
    steps/train_sat_basis.sh --cmd "$cmd" 22000 450000 $train_dir $lang_dir exp/tri8_ali exp/tri9

fi
#####################################################################################################################



############################################ LDA-MLLT Triphones Training ############################################
if [ $stage -le 15 ]; then  
    echo "####################################### LDA-MLLT Triphones Training #######################################"
    echo "$0: TENTH triphone training"

    #Align SAT triphones with FMLLR
    steps/align_basis_fmllr.sh  --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri9 exp/tri9_ali

    #train third pass of LDA-MLLT
    steps/train_lda_mllt.sh --cmd "$cmd" 25000 500000 $train_dir $lang_dir exp/tri9_ali exp/tri10
fi
#####################################################################################################################



############################################### SAT Triphones Training ##############################################
if [ $stage -le 16 ]; then
    echo "########################################## SAT Triphones Training #########################################"
    echo "$0: ELEVENTH triphone training"

    #Align LDA-MLLT triphones with FMLLR
    steps/align_fmllr.sh --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri10 exp/tri10_ali
    
    #Train SAT triphones
    steps/train_sat_basis.sh --cmd "$cmd" 28000 550000 $train_dir $lang_dir exp/tri10_ali exp/tri11

    #Align SAT triphones with FMLLR
    steps/align_basis_fmllr.sh  --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri11 exp/tri11_ali

    echo "$0: Creating graph and Decoding"
    #decoding
    utils/mkgraph.sh $lang_test_dir exp/tri11 exp/tri11/graph || exit 1;
    steps/decode_basis_fmllr.sh --nj $nj --cmd "$cmd" exp/tri11/graph $test_dir exp/tri11/decode_test

fi
#####################################################################################################################





#################################################### NNET Training ###################################################
if [ $stage -le 17 ]; then
    echo "$0: Starting nnet training"
    state=$(nvidia-smi  --query | grep 'Compute Mode')
    state=($state)
    state=${state[3]}
    if [ ! "$state" == "Exclusive_Process" ]; then
      echo "Please set the compute mode to Exclusive_Process using 'nvidia-smi -c 3' "
      exit 1
    else
      echo "Successfully set compute mode to Exclusive_Process"
    fi
    CUDA_VISIBLE_DEVICES=0,1 local/nnet3/run_tdnn_lstm.sh
fi
#####################################################################################################################