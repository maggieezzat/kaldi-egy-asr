#!/usr/bin/env bash

SECONDS=0

data="dev1h"
data_dir="data/"$data

nnet3_affix=_tdnn_lstm_train

cmd="run.pl"
nj=1
################################################## Feature Extraction ###############################################
sort -u -o $data_dir/wav.scp $data_dir/wav.scp
sort -u -o $data_dir/text $data_dir/text
sort -u -o $data_dir/utt2spk $data_dir/utt2spk

#make spk2utt file
utils/utt2spk_to_spk2utt.pl $data_dir/utt2spk > $data_dir/spk2utt

#fix data directory
utils/fix_data_dir.sh $data_dir

log_dir="$data_dir/log"
mfcc_dir="$data_dir/mfcc"
vad_dir="$data_dir/vad"
segments_dir="$data_dir/segments"
cmvn_dir="$data_dir/cmvn"
steps/make_mfcc.sh --mfcc-config conf/mfcc.conf --nj $nj --cmd "$cmd" --write-utt2num-frames true $data_dir $log_dir $mfcc_dir || exit 1;

#fix data directory
utils/fix_data_dir.sh $data_dir 

#compute cepstral mean and variance statistics per speaker.
steps/compute_cmvn_stats.sh $data_dir $log_dir $cmvn_dir || exit 1;

#fix data directory
utils/fix_data_dir.sh $data_dir

utils/copy_data_dir.sh $data_dir ${data_dir}_hires

#high res features
steps/make_mfcc.sh --nj $nj --mfcc-config conf/mfcc_hires.conf --cmd "$cmd" ${data_dir}_hires
steps/compute_cmvn_stats.sh ${data_dir}_hires
utils/fix_data_dir.sh ${data_dir}_hires

#ivectors
steps/online/nnet2/extract_ivectors_online.sh --cmd "$cmd" --nj $nj \
      ${data_dir}_hires exp/nnet3${nnet3_affix}/extractor exp/nnet3${nnet3_affix}/ivectors_${data}_hires
#####################################################################################################################

echo "$(($SECONDS / 60)) minutes and $(($SECONDS % 60)) seconds for extracting features" >> dec_time.txt

extr_time=$SECONDS

SECONDS=0

#looped decoding
data_affix=$(echo $data | sed s/test_//)

affix=1a
dir=exp/nnet3${nnet3_affix}/tdnn_lstm${affix}_sp

graph_dir=exp/tri11/graph
steps/nnet3/decode_looped.sh \
        --frames-per-chunk 30 \
        --nj $nj --cmd "$cmd" \
        --online-ivector-dir exp/nnet3${nnet3_affix}/ivectors_${data}_hires \
        $graph_dir ${data_dir}_hires ${dir}/decode_looped_${data_affix}


echo "$(($SECONDS / 60)) minutes and $(($SECONDS % 60)) seconds for decoding" >> dec_time.txt
total=$(($SECONDS + $extr_time))
echo "Total time is $(($total / 60)) minutes and $(($total % 60)) seconds" >> dec_time.txt

