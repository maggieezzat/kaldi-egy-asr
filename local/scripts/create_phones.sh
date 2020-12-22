#!/usr/bin/env bash

dict_dir_nosp=$1

mkdir -p $dict_dir_nosp

echo 'SIL' > $dict_dir_nosp/optional_silence.txt
echo 'SIL' > $dict_dir_nosp/silence_phones.txt
echo '<UNK>' > $dict_dir_nosp/nonsilence_phones.txt
echo 'A' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'B' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'C' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'D' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'E' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'F' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'G' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'H' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'I' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'J' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'K' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'L' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'M' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'N' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'O' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'P' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'Q' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'R' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'S' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'T' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'U' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'V' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'W' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'X' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'Y' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'Z' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'a' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'b' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'c' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'd' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'e' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'f' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'g' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'h' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'i' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'j' >> $dict_dir_nosp/nonsilence_phones.txt
echo 'music_noise' >> $dict_dir_nosp/nonsilence_phones.txt