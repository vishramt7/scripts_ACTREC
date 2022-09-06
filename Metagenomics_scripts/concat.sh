#! /usr/bin/bash

path=$1
output=batch2.dat

lines=0
> ${output}
for i in `ls ${path}/*taxa.tsv.populatn`
do 
	file=$(basename ${i} -taxa.tsv.populatn)
	file2="temp.dat"
	echo -e "${file}\tproportion" > ${file2}
	cat ${i} >> ${file2}
#	cp ${output} temp2.dat

#	file1="temp2.dat"
	file1_lines=$(wc -l ${file2} | awk '{print $1}')
#	file2_lines=$(wc -l ${file2} | awk '{print $1}')

#	if [ ${file2_lines} -gt ${file1_lines} ] && [ ${file1_lines} -gt 0 ]; then
#        extra_lines=$( echo "${file2_lines} - ${file1_lines}" | bc )
#		for (( j=1; j<=${extra_lines}; j++ ))
#		do
#			echo -e "-\t-" >> ${file1}
#			#echo "adding for ${i}"
#		done
#		echo "adding for ${i}"
#	fi
	if [ ${file1_lines} -gt ${lines} ] ; then
		lines=${file1_lines}
	fi
#	#paste <(sed 's/^[[:blank:]]*//' temp2.dat ) temp.dat > ${output}
done
echo "${lines}"


for j in `ls ${path}/*taxa.tsv.populatn`
do
	file=$(basename ${j} -taxa.tsv.populatn)
	file2="temp.dat"
	echo -e "${file}\tproportion" > ${file2}
	cat ${j} >> ${file2}
	cp ${output} temp2.dat
	file1="temp2.dat"

	file1_lines=$(wc -l ${file2} | awk '{print $1}')
	extra_lines=$( echo "${lines} - ${file1_lines}" | bc )
	for (( k=1; k<=${extra_lines}; k++ ))
	do
		echo -e "-\t-" >> ${file2}		
	done

	paste ${file1} ${file2} > ${output}
done
rm temp.dat temp2.dat
