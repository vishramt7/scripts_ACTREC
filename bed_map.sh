#! /usr/bin/bash

samplesheet=$1

for i in `cat ${samplesheet}`
do
        bed=$( echo ${i} | awk 'BEGIN{FS="-";OFS=""}{ $1="" ; print tolower($2)}' )
        case $bed in
                "ball" | "kmt2a" | "ball_tall" | "znf384" | "pax5etv6" | "dux4" | "fgfr1" | "crlf2" | "crlf2tcf3" | "p190")
                bedfile="/data/home2/hematopath/hemoseq_v2/fusion_seq_noumi/bed/BALLlymphoid_fusion02062022.bed"
                ;;
                "tall")
                bedfile="/data/home2/hematopath/hemoseq_v2/fusion_seq_noumi/bed/T-ALL02062022.bed"
                ;;
                "myfu" | "eofu" | "nup98" | "kmt2a")
                bedfile="/data/home2/hematopath/hemoseq_v2/fusion_seq_noumi/bed/myeloid_fusion02062022.bed"
                ;;
                *)
                echo "could not map the panel name to a directory, ${i} ${bed}"
                exit 1
        esac
	#echo "${i},${bedfile}" >> ${samplesheet}_bedmap
	echo "${i},/data/home2/hematopath/hemoseq_v2/fusion_seq_noumi/analysis/17Oct22,/data/home2/hematopath/hemoseq_v2/fusion_seq_noumi/sequences/17Oct22,15,${bedfile}" >> ${samplesheet}_bedmap
done

