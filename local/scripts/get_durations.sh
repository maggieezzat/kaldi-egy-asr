#!/usr/bin/env bash

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################

while read file_id file_name; do
  f="waves/all_waves/$file_name"
  dur=$(sox $f -n stat 2>&1 | sed -n 's#^Length (seconds):[^0-9]*\([0-9.]*\)$#\1#p')
  echo $file_id $file_name $dur >> local/data/wav_msa_durations.txt
done <local/data/wav_msa.scp