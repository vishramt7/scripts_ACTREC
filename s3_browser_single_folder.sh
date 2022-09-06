#!/usr/bin/env bash

path_to_fastq="/home/wtp_server_backup_runs/210902_M04898_0182_000000000-JVD6J/Data/Intensities/BaseCalls"
AML_folder="MISCELLANEOUS_miseq_210902.dat"
#AML_folder="211018_ALP"

# Make a folder and copy the fastq.gz files here
mkdir ${AML_folder}
#rsync -a ${path_to_fastq}/AR*fastq* ${AML_folder}/	# The fastq needs to match the full sample name
#mv ${path_to_fastq}/DrSonaliPatkar*fastq* ${AML_folder}/
#mv ${path_to_fastq}/AlkaWarade*fastq* ${AML_folder}/
#mv ${path_to_fastq}/KNWarade*fastq* ${AML_folder}/

# Copying the data to respective folders needs to be verified
#if [ $? -eq 0 ]; then
#	echo "copied successfully"
#else
#	echo "copying failed"
#fi

# Search for fastq files and choose only the ones without a digit at their start and move them to a folder named in MISC
#for i in `ls $path_to_fastq/*fastq* | sed "s:$path_to_fastq/::g" | grep -E '^[^0-9]+' | grep -v 'Undetermined*'`
#do
#	file_name=$(basename $i)
#	echo $file_name $AML_folder
#	mv $path_to_fastq/$file_name $AML_folder/
#done

exit_stat=1
while [ $exit_stat -ne 0 ]; do
	aws s3 sync ${AML_folder} s3://hematopath-data/Clinical_NGS_Analysis/01FastqArchival2021/${AML_folder}/
	exit_stat=$?
done
echo "`ls ${AML_folder}/*` synced to hematopath-data/Clinical_NGS_Analysis/01FastqArchival2021/${AML_folder}" >> miseq_210902.dat.info
