#! /usr/bin/bash 
# This script will initiate the nf-core/rnafusion pipeline. The input is samplesheet.csv

samplesheet=$1
log_file=$2
sequences="/home/diagnostics/pipelines/nf-core/rnafusion/samples"

echo "sample,fastq_1,fastq_2,strandedness" > samplesheet.csv
for samples in `cat ${samplesheet}`
do 
	mkdir -p Final_Output/${samples}
	R1=$(ls $sequences/${samples}_S* | grep -i '_R1_')
	R2=$(ls $sequences/${samples}_S* | grep -i '_R2_')
	echo "$samples,$R1,$R2,forward" >> samplesheet.csv	
done 

nextflow run ./ --all --input samplesheet.csv --outdir /home/diagnostics/pipelines/nf-core/rnafusion --genome GRCh38 -profile docker -resume > ${log_file}

touch ${samplesheet}_bedmap
for i in `cat ${samplesheet}`
do
	bed=$( echo ${i} | awk 'BEGIN{FS="-";OFS=""}{ $1="" ; print tolower($0)}' )
	case $bed in
		"ball" | "kmt2a" | "ball_tall")
		bedfile="/home/diagnostics/pipelines/nf-core/rnafusion/bedfiles/BALLlymphoid_fusion02062022.bed"
		;;
		"tall")
		bedfile="/home/diagnostics/pipelines/nf-core/rnafusion/bedfiles/T-ALL02062022.bed"
		;;
		"myfu")
		bedfile="/home/diagnostics/pipelines/nf-core/rnafusion/bedfiles/myeloid_fusion02062022.bed"
		;;
		*)
		echo "could not map the panel name to a directory, ${i} ${bed}"
		exit 1
	esac
echo "${i},${bedfile}" >> ${samplesheet}_bedmap
done

nextflow -C /home/diagnostics/pipelines/nf-core/rnafusion/scripts/custom.config run /home/diagnostics/pipelines/nf-core/rnafusion/scripts/custom.nf -entry COVERAGE -resume --input ${samplesheet}_bedmap > ${log_file}.coverage

for samples in `cat ${samplesheet}`
do
	cp arriba/${samples}.arriba.fusions.tsv arriba_visualisation/${samples}.pdf Final_Output/${samples}
	cp squid/${samples}.squid.*.txt Final_Output/${samples}
	cp pizzly/${samples}.pizzly.txt Final_Output/${samples}
	cp fusioncatcher/${samples}.fusioncatcher.fusion-genes.txt fusioncatcher/${samples}.fusioncatcher.summary.txt Final_Output/${samples}
	cp starfusion/${samples}.starfusion.fusion_predictions.tsv Final_Output/${samples}
	cp -r fusionreport/${samples} Final_Output/${samples}/${samples}_fusionreport
done
