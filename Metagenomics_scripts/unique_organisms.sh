#!/usr/bin/bash

sample_file=$1
org_to_remove=$2

for i in `cat ${sample_file}`
do
	sample=$(echo ${i} | awk 'BEGIN{FS=","}{print $1}')
	./cancervar_extract.py ${org_to_remove} ${sample}-taxa.tsv.micro_populatn temp.dat
	grep -w -f temp.dat ${sample}-taxa.tsv | awk 'BEGIN{FS=OFS="\t"}{if ($4=="S") print $6,$2}' | sed 's/^[ ]\+//g' |  awk 'BEGIN{FS=OFS"\t"}{print $1,$2}' | sort -t $'\t' -k2,2rn > ${sample}_ntc_bnc_all.tsv

done
