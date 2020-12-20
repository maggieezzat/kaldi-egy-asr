#!/usr/bin/env bash

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################

train="data/train/wav.scp"
test="data/test/wav.scp"
dev="data/dev/wav.scp"

mkdir -p waves/used_waves

for x in $dev $test $train; do
    echo $x
    while read id path ;
    do
        path='waves/all_waves/'$id'.wav'
        rsync -aXS $path waves/used_waves
    done < $x
done
