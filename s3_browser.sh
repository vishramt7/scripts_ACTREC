#!/usr/bin/env bash

fastq_file_csv=$1
path_to_fastq=$2
#year=$(date +%Y)

echo "The input file must be a csv, else panel name extraction will be errorneous"
no_of_runs_from_csv=$(wc -l ${fastq_file_csv} | awk '{print $1}')
no_of_fastq=$(ls ${path_to_fastq}/*.fastq.gz | grep -v 'Undetermined' | wc -l )	# Removing the undetermined fastq.gz
expected_fastq=$(echo "${no_of_runs_from_csv} * 2" | bc -l )

no_of_panels=$(cat ${fastq_file_csv} | awk 'BEGIN{FS=","} {print $2}' | sort | uniq )
echo "The panels present are ${no_of_panels}" >> ${fastq_file_csv}.info
echo "No. of samples are ${no_of_runs_from_csv}, no. of fastq files are ${no_of_fastq} " >> ${fastq_file_csv}.info

if [ ${no_of_fastq} -eq ${expected_fastq} ]; then
	echo "No. of fastq files in the folder are equal to the samples"
else
	echo "WARNING: No. of fastq.gz files in the folder are not equal to the samples, please check!!"
fi

for (( i=1; i<=${no_of_runs_from_csv}; i++ ))
do 
	sample_name=$(awk -v line_no="${i}" 'BEGIN{FS="[, _-]"} NR==line_no {print $1}' ${fastq_file_csv})
	sample_name_full=$(awk -v line_no="${i}" 'BEGIN{FS="[, ]"} NR==line_no {print $1}' ${fastq_file_csv})
	sample_name_append=$(echo ${sample_name_full} | sed -r s/${sample_name}//g)
	panel_name=$(awk -v line_no="${i}" 'BEGIN{FS="[,]"} NR==line_no {print tolower($2)}' ${fastq_file_csv} | sed 's/[-_]/ /g')

	# Identifying the sample year
	sample_description=$(echo ${sample_name} | sed -r 's/[0-9]*//g')	# Removing all digits
	sample_year=${sample_name:0:2}									# First 2 characters specify the year
	sample_id=$(echo ${sample_name} | sed -r 's/^[0-9][0-9]//g')	# id without the year 
	sample_number=$(echo ${sample_id} | sed -r 's/[^0-9]*//g')		# extracting the sample number
	sample_number_formatted=$( printf "%04d" ${sample_number})		# Sample number needs to be 4 digit
	year="20${sample_year}"

	# Check for panel name, write a case statement here for various panel names
	case $panel_name in
		"leukemia panel" | "leukemia panel val" | "alp" | "acute leukemia panel")
		panel_dir="ALP"
		;;
		"narsimha" | "amp" | "narasimha" | "nv2 diagnostic")
		panel_dir="NARSIMHA"
		;;
		"narsimha v2" | "nv2" | "narasimha v2 ")
		panel_dir="NARSIMHA_V2"
		;;
		"mips")
		panel_dir="MIPS"
		;;
		"mrd")
		panel_dir="MRD"
		;;
		"srsf2")
		panel_dir="SRSF2"
		;;
		"duplex")
		panel_dir="DUPLEX"
		;;
		"kdm")
		panel_dir="KDM"
		;;
		"npm1")
		panel_dir="NPM1"
		;;
		"cebpa mrd" | "cebpamrd")
		panel_dir="CEBPA_MRD"
		;;
		"clligvh" | "cll igvh")
		panel_dir="CLLIGVH"
		;;
		"npm1mrd" | "npm1 mrd")
		panel_dir="NPM1MRD"
		;;
		"flt3")
		panel_dir="FLT3"
		;;
		"igvh")
		panel_dir="IGVH"
		;;
		"usg")
		panel_dir="USG"
		;;
		"cll" | "cll mips" | "mipscll")
		panel_dir="CLL"
		;;
		"flt3mrd")
		panel_dir="FLT3MRD"
		;;
		"new mrd panel")
		panel_dir="NEW_MRD_PANEL"
		;;
		"cebpa")
		panel_dir="CEBPA"
		;;
		"lsc")
		panel_dir="LSC"
		;;
		"mips mrd")
		panel_dir="MIPS_MRD"
		;;
		*)
		echo "could not map the panel name to a directory, ${sample_name} $panel_name"
		exit 1
	esac
		
	# Check if the sample is from Varanasi
	if [[ ${sample_id} =~ ^[V] ]];then
		#echo "Varanasi sample: ${sample_name} ${panel_name} ${sample_year} ${sample_id} ${sample_number_formatted}"
		s3_varanasi_folder="VARANASI_${year}/"
	else
		#echo "TMC/TMH sample : ${sample_name} ${panel_name} ${sample_year} ${sample_id} ${sample_number_formatted}"
		s3_varanasi_folder=""
	fi

	folder_name="${sample_year}${sample_description}${sample_number_formatted}${sample_name_append}"

	# Make a folder and copy the fastq.gz files here
	mkdir -p ${folder_name}/${panel_dir}
	#rsync -a ${path_to_fastq}/${sample_name_full}_S*fastq* ${folder_name}/${panel_dir}	# The fastq needs to match the full sample name
	mv ${path_to_fastq}/${sample_name_full}_S*fastq* ${folder_name}/${panel_dir}/
	# ls ${folder_name}/${panel_dir}

	# Copying the data to respective folders needs to be verified
	if [ $? -eq 0 ]; then
		echo "copied ${folder_name} successfully"
	else
		echo "copying for ${folder_name} failed"
		exit 1
	fi

	#Check if the file is already present at the location
	check_stat=1
	while [ $check_stat -ne 0 ]; do
		aws s3 ls hematopath-data/Clinical_NGS_Analysis/01FastqArchival${year}/ --recursive > ${fastq_file_csv}_s3_files.dat
		check_stat=$?
	done

	for j in `ls ${folder_name}/${panel_dir} | sed "s:${folder_name}/${panel_dir}::g"`
	do 
		fastq_file_name=$(basename $j)
		if grep "/${folder_name}/${panel_dir}/$fastq_file_name" ${fastq_file_csv}_s3_files.dat ; then
			echo "ERROR: File $fastq_file_name is already present in the destination, exiting" >> ${fastq_file_csv}.info
			exit 1
		fi
	done


	# Irrespective of the presence of the folder on s3, it is safe to do a sync instead of mv or cp
	aws s3 sync ${folder_name} s3://hematopath-data/Clinical_NGS_Analysis/01FastqArchival${year}/${s3_varanasi_folder}${folder_name}/
	while [ $? -ne 0 ]; do
		aws s3 sync ${folder_name} s3://hematopath-data/Clinical_NGS_Analysis/01FastqArchival${year}/${s3_varanasi_folder}${folder_name}/
	done 

	fastq_files=$(ls ${folder_name}/*)
	echo "${fastq_files} synced to hematopath-data/Clinical_NGS_Analysis/01FastqArchival${year}/${s3_varanasi_folder}${folder_name}/" >> ${fastq_file_csv}.info
	rm -r ${folder_name}
done

# aws s3 ls hematopath-data/Clinical_NGS_Analysis/01FastqArchival2022/22NGS0001/
# aws s3api put-object --bucket hematopath-data --key Clinical_NGS_Analysis/01FastqArchival2022/21NGS1064/

# please note you need to add a trailing / to make sure the newly created object is a folder, otherwise a file will be created.
# aws s3 cp /home/wtp_server_backup_runs/211209_VL00151_6_AAANGVYM5/Analysis/1/Data/fastq/21NGS1064_S56_R2_001.fastq.gz s3://hematopath-data/Clinical_NGS_Analysis/01FastqArchival2022/21NGS1064/ALP/

# aws s3 sync temp s3://hematopath-data/Clinical_NGS_Analysis/01FastqArchival2021/Check/temp/ # Make sure to add the directory at the end of the path to create a new one, This will sync the contents of the temp directory with the temp directory
# number_of_files_s3=$(aws s3 ls hematopath-data/Clinical_NGS_Analysis/01FastqArchival${year}/${s3_varanasi_folder}${folder_name}/ --recursive --summarize | grep "Total Objects: " | sed 's/[^0-9]*//g')
