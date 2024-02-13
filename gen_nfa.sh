#!/bin/bash

./hibou_label.exe glosem ./model/hibou_para.hsf ./output/hif_files/${1}.hif
cp ${1}_orig_nfa.dot ./output/dot_files/${1}.dot
cp ${1}
rm *.png
rm *.dot
rm *.svg