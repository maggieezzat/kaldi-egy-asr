#!/usr/bin/env bash

n=1
lattice_dir="exp/tri6/decode_test"
lang_dir="data/lang"

gunzip -c $lattice_dir/lat.1.gz |\
lattice-to-nbest --acoustic-scale=0.0883 --n=$n ark:- ark:- | \
nbest-to-ctm --precision=4 ark:- - | utils/int2sym.pl -f 5 $lang_dir/words.txt > $lattice_dir/NBest.$n.ctm || exit 1;
