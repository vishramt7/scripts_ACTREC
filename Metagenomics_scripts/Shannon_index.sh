#!/usr/bin/bash

sample_file=$1

for i in `cat ${sample_file}`
do
	sample=$(echo ${i} | awk 'BEGIN{FS=","}{print $1}')
	shannon_index=$(./Shannon_index_norm.py ${sample}-taxa.tsv)
	echo -e "${sample}\t${shannon_index}"
done
