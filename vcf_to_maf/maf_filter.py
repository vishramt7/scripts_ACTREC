#!/usr/bin/env python3
# This script will filter the variants in the maf file.
# The input is a file containing sample list (*.somaticseq.vcf and *.vep.maf ) and the output is *.filt.maf file

import os
import csv
import sys
import subprocess
import re

infile = sys.argv[1]    # File with sample names

# Columns to screen
PopFreqMax = "PopFreqMax"
popfreqlimit = 0.01
FuncrefGene = "Func.refGene"
ExonicFuncrefGene = "ExonicFunc.refGene"
# Strings to search
exonic_splice = "exonic|splic"
synonymous = r"\bsynonymous"
# Columns to screen in maf file
Chromosome = "Chromosome"
Start_Position = "Start_Position"
End_Position = "End_Position"
Reference_Allele = "Reference_Allele"
Tumor_Seq_Allele2 = "Tumor_Seq_Allele2"	# In a maf file, the alt allele is present in the "Tumor_Seq_Allele2" column

if os.path.getsize(infile) != 0:
	with open (infile,'r') as f:
		csv_handle = csv.reader(f)
		for samples in csv_handle:
			lines = samples[0]

			vcf_file = lines+".somaticseq.vcf"
			avinput_file = lines+".somaticseq.avinput"
			avinput_cmd = ["/home/programs/annovar_latest/annovar/convert2annovar.pl", "-format", "vcf4", vcf_file, "--outfile", avinput_file, "--withzyg", "--includeinfo"]
			subprocess.run(avinput_cmd)

			SomaticSeq_output = lines+".somaticseq"
			annotate_cmd = ["/home/programs/annovar_latest/annovar/table_annovar.pl", avinput_file, "--out", SomaticSeq_output, "--remove", "--protocol", "refGene,cytoBand,cosmic84,popfreq_all_20150413,avsnp150,intervar_20180118,1000g2015aug_all,clinvar_20170905", "--operation", "g,r,f,f,f,f,f,f", "--buildver", "hg19", "--nastring", "'-1'", "--otherinfo", "--csvout", "--thread", "10", "/home/programs/annovar_latest/annovar/humandb/", "--xreffile", "/home/programs/annovar_latest/annovar/example/gene_fullxref.txt"]
			subprocess.run(annotate_cmd)
			#print (annotate_cmd)

			# Filter the output of annovar for conditions on PopfreqMax and others
			Filtered_dict = dict()
			SomaticSeqCsv = SomaticSeq_output+".hg19_multianno.csv"
			if os.path.getsize(SomaticSeqCsv) != 0:
				with open (SomaticSeqCsv,'r') as annovar_output:
					annovar_csv_handle = csv.reader(annovar_output)
					header = next (annovar_csv_handle)
					for csv_lines in annovar_csv_handle:
						popfreq = float(csv_lines[header.index(PopFreqMax)].strip("'"))
						funcrefgene = str(csv_lines[header.index(FuncrefGene)])
						exonicfuncrefgene = str(csv_lines[header.index(ExonicFuncrefGene)])
						chrm = csv_lines[0]
						start = csv_lines[1]
						end = csv_lines[2]
						ref = csv_lines[3]
						alt = csv_lines[4]

						if popfreq < popfreqlimit:	# Remove variants with freq < popfreqlimit
							if re.search(exonic_splice, funcrefgene, flags = re.IGNORECASE):	# Select variants which have 'exonic_splice' enteries
								if not re.search(synonymous, exonicfuncrefgene, flags = re.IGNORECASE): # Remove variants other than 'synonymous'
									map_id = str(chrm) + ':' +''.join(str(start)) + ':' +''.join(str(end)) + ':' +''.join(str(ref)) + ':' +''.join(str(alt))
									#print (map_id)
									Filtered_dict[map_id] = 1


			# Mapping it to the maf file
			maf_file = lines+".vep.maf"
			maf_outfile_name = lines+".filt.maf"
			output_file = open (maf_outfile_name,'w')
			if os.path.getsize(maf_file) != 0:
				with open (maf_file, 'r') as maf:
					maf_handle = csv.reader(maf, delimiter = '\t')
					head1 = next (maf_handle)
					head2 = next (maf_handle)
					print (*head1, file=output_file, sep="\t")
					print (*head2, file=output_file, sep="\t")
					for maf_lines in maf_handle:
						chrom_maf = str(maf_lines[head2.index(Chromosome)])
						start_maf = str(maf_lines[head2.index(Start_Position)])
						end_maf = str(maf_lines[head2.index(End_Position)])
						ref_maf = str(maf_lines[head2.index(Reference_Allele)])
						alt_maf = str(maf_lines[head2.index(Tumor_Seq_Allele2)])

						maf_id = str(chrom_maf) + ':' +''.join(str(start_maf)) + ':' +''.join(str(end_maf)) + ':' +''.join(str(ref_maf)) + ':' +''.join(str(alt_maf))
						if maf_id in Filtered_dict:
							print (*maf_lines, file=output_file, sep="\t")

			Filtered_dict.clear()
			output_file.close()
