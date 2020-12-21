#!/usr/bin/env bash

dict_dir_nosp=$1

mkdir -p $dict_dir_nosp

echo 'SIL' > data/local/dict_nosp/optional_silence.txt
echo 'SIL' > data/local/dict_nosp/silence_phones.txt
echo '<UNK>' > data/local/dict_nosp/nonsilence_phones.txt
echo 'A' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'B' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'C' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'D' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'E' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'F' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'G' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'H' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'I' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'J' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'K' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'L' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'M' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'N' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'O' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'P' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'Q' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'R' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'S' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'T' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'U' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'V' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'W' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'X' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'Y' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'Z' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'a' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'b' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'c' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'd' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'e' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'f' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'g' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'h' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'i' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'j' >> data/local/dict_nosp/nonsilence_phones.txt
echo 'music_noise' >> data/local/dict_nosp/nonsilence_phones.txt