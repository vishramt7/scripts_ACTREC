#! /usr/bin/env bash

annovar_input_file=$1
sample=$2
cancervar_infile=${sample}_cancervar_input.dat
cancervar_outprefix=${sample}myanno

source activate new_base
/home/pipelines/NextSeq_mutation_detector_leukemia/scripts/cancervar_input.py ${annovar_input_file} ${cancervar_infile}

cp /home/programs/CancerVar/config.ini config.ini
sed -i -r "s/inputfile = .*/inputfile = ${cancervar_infile}/g" config.ini
sed -i -r "s/outfile = .*/outfile = ${cancervar_outprefix}/g" config.ini
python3 /home/programs/CancerVar/CancerVar.py -c config.ini

python3 /home/programs/CancerVar/OPAI/scripts/feature_preprocess.py -a ${cancervar_outprefix}.hg19_multianno.txt.grl_p -c ${cancervar_outprefix}.hg19_multianno.txt.cancervar -m ensemble -n 5 -d /home/programs/CancerVar/OPAI/saves/nonmissing_db.npy -o ${cancervar_outprefix}.hg19_multianno.txt.cancervar.ensemble.csv

python3 /home/programs/CancerVar/OPAI/scripts/opai_predictor.py -i ${cancervar_outprefix}.hg19_multianno.txt.cancervar.ensemble.csv -m ensemble -c /home/programs/CancerVar/OPAI/saves/ensemble.pt -d cpu -v ${cancervar_outprefix}.hg19_multianno.txt.cancervar -o ${cancervar_outprefix}.hg19_multianno.txt.cancervar.ensemble.pred
