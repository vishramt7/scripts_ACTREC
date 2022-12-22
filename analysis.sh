#! /usr/bin/bash 
# This script will concatenate the raw counts for all the samples in a run to a tab separated file named concat.dat

folder_name="13Dec22"
sample_list="sample_list1"

>concat.dat
for i in `cat ${sample_list}`
do 
	if [ ! -s ${folder_name}/$i/$i.*.rawcounts.sorted.txt ]
	then
		#echo "$i is empty"	
		for i in {0..16}; do echo 0; done > temp.dat	# printing value = 0 for the first 17 genes
	else
		#echo "$i is not empty"
		head -n17 ${folder_name}/$i/$i.*.rawcounts.sorted.txt | awk '{print $2}' > temp.dat	
	fi
	
	cp concat.dat concat_temp.dat 
	paste concat_temp.dat temp.dat > concat.dat
done

>concat_abl.dat
for i in `cat ${sample_list}`
do
	~/programs/subread-2.0.2-source/bin/featureCounts -p -a /scratch/hematopath/testing/LSC_stemness/ensembl_genome/subset_17genes_ABL.gtf -o ${folder_name}/$i/${i}".subset.readcounts_abl1.txt" ${folder_name}/$i/${i}".bwt.sorted.bam"
	awk 'FNR>2 {print $1, $NF}' ${folder_name}/$i/${i}".subset.readcounts_abl1.txt" > ${folder_name}/$i/${i}".subset.rawcounts_abl1.txt"
	sort ${folder_name}/$i/${i}".subset.rawcounts_abl1.txt" > ${folder_name}/$i/${i}".subset.rawcounts_abl1.sorted.txt"
	sed -i 's/ /\t/g' ${folder_name}/$i/${i}".subset.rawcounts_abl1.sorted.txt"

	if [ ! -s ${folder_name}/$i/$i.*.rawcounts_abl1.sorted.txt ]
	then
		echo 0 > temp.dat
	else
		grep 'ENSG00000097007' ${folder_name}/$i/$i.*.rawcounts_abl1.sorted.txt | awk '{print $2}' > temp.dat
	fi

	cp concat_abl.dat concat_temp.dat
	paste concat_temp.dat temp.dat > concat_abl.dat
done

>concat_bed.dat
for i in `cat ${sample_list}`
do
	if [ ! -s ${folder_name}/$i/${i}.counts.bed ]
	then
		for i in {0..16}; do echo 0; done > temp.dat
	else
		awk 'BEGIN{FS="\t"}{print $5}' ${folder_name}/${i}/${i}.counts.bed > temp.dat
	fi

	cp concat_bed.dat concat_bed_temp.dat
	paste concat_bed_temp.dat temp.dat > concat_bed.dat
done

#Bed file to Interval file
#java -jar ~/programs/picard-tools-2.17.1/picard-2.17.1.jar BedToIntervalList I=/scratch/hematopath/testing/LSC_stemness/test_analysis/bedfile/capture_probes.bed O=/scratch/hematopath/testing/LSC_stemness/test_analysis/bedfile/capture_probes.interval.list SD=/scratch/hematopath/testing/LSC_stemness/ensembl_genome/Homo_sapiens.GRCh38_r104.all.dict

>hs_metrics.dat
for i in `cat ${sample_list}`
do
	java -jar ~/programs/picard-tools-2.17.1/picard-2.17.1.jar CollectHsMetrics I=/scratch/hematopath/testing/LSC_stemness/test_analysis/${folder_name}/$i/${i}.bwt.sorted.bam O=/scratch/hematopath/testing/LSC_stemness/test_analysis/${folder_name}/${i}.hsmetrics.txt R=/scratch/hematopath/testing/LSC_stemness/ensembl_genome/Homo_sapiens.GRCh38_r104.all.fa BAIT_INTERVALS=/scratch/hematopath/testing/LSC_stemness/test_analysis/bedfile/capture_probes.interval.list TARGET_INTERVALS=/scratch/hematopath/testing/LSC_stemness/test_analysis/bedfile/capture_probes.interval.list VALIDATION_STRINGENCY=LENIENT
	
	echo -ne $i'\t' >> hs_metrics.dat
	grep -v '#' /scratch/hematopath/testing/LSC_stemness/test_analysis/${folder_name}/${i}.hsmetrics.txt | awk 'BEGIN{FS="\t"; OFS="\t"}NR==3{ print $19,$20}' >> hs_metrics.dat

done

./lsc_score.py ${sample_list} ensemble_genesymbol_weights.txt ${folder_name}
