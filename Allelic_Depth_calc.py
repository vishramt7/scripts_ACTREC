#!/usr/bin/env python
# This script will take a .vcf file as input and calculate Allelic Depth 
# The output will be a .vcf file with AD values included
# AD will be calculated using DP4 values

import sys
import re
import csv
import os

somaticseq_vcf = sys.argv[1]	# input file obtained from somatiseq
output_vcf = sys.argv[2]		# output vcf file 

output_vcf = open (output_vcf,'w')
ad_header='##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">'
ref_values = ""
alt_values = ""
format_col = "FORMAT"
DP4_header = "FORMAT=<ID=DP4"

if os.path.getsize(somaticseq_vcf) != 0:
	with open (somaticseq_vcf,'r') as f:
		for lines in f:
			if lines.startswith("#"):
				print (lines, file=output_vcf, end="")
				if DP4_header in lines:
					print (ad_header, file=output_vcf)	# Adding a line describing AD header

				if lines.startswith("#CHROM") and format_col in lines:
					format_colmn_index = (lines.split('\t')).index(format_col)	# This helps to obtain the index of the FORMAT column
			else:
				format_column = lines.split('\t')[format_colmn_index]
				format_column_split = format_column.split(':')
				if "DP4" in format_column_split:
					dp4_value_index = format_column_split.index("DP4")			# Obtain the index of the DP4 values
					# Analyze the data column
					data_column = lines.split('\t')[format_colmn_index + 1]
					data_column_split = data_column.split(':')
					dp4_values_list = (data_column_split[dp4_value_index]).split(',')
					len_dp4_values_list = len (dp4_values_list)
		
					if len_dp4_values_list > 4:
						print ("WARNING : MORE THAN ONE REF / ALT allele", dp4_values_list)

					AD_list = list()
					for i in range (0,len_dp4_values_list, 2):
						ad_values = int (dp4_values_list[i]) +  int (dp4_values_list[i+1])
						AD_list.append(ad_values)

					# Add "AD" to the format column
					format_column_split.insert(dp4_value_index + 1, "AD")
					format_column_split = str(format_column_split)[1:-1]
					format_column_split = re.sub ("'","", format_column_split, flags = re.IGNORECASE)
					new_format_column = format_column_split.replace(', ',':')

					# Add "AD" values to the data column
					AD_list = str(AD_list)[1:-1]
					AD_list = AD_list.replace(', ',',')
					data_column_split.insert(dp4_value_index + 1, AD_list)
					data_column_split = str (data_column_split)[1:-1]
					data_column_split = re.sub ("'","", data_column_split, flags = re.IGNORECASE)
					new_data_column = data_column_split.replace(', ',':')

					new_line = re.sub (format_column , new_format_column, lines, flags = re.IGNORECASE)
					new_line = re.sub (data_column, new_data_column, new_line, flags = re.IGNORECASE)

					print (new_line, file=output_vcf, end="")

				else:
					print (lines, file=output_vcf, end="")
else:
	print ("File not found")
	sys.exit ()

output_vcf.close ()
