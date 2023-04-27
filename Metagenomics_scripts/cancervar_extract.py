#! /usr/bin/env python3

import sys
import csv
import re

cancervar_file = sys.argv[1]# file with organisms to be removed
vep_file = sys.argv[2]		# file with organisms and their proportion
output_file = sys.argv[3]	# output file

map_evidence = dict()		# Dictionary for the cancervar evidence
map_ensembl_score = dict()	# Dictionary for score
with open (cancervar_file, 'r') as tsv_file:
	cancervar_handle = csv.reader(tsv_file, delimiter = '\t')
	for vep_values in cancervar_handle:
		chrom = vep_values[0].lower()
		#print (chrom)
		map_ensembl_score[chrom] = 1
	
outfile = open (output_file, 'w')
with open (vep_file,'r') as vcf:
	csv_handle = csv.reader(vcf, delimiter = '\t')
	for str_lines in csv_handle:
		name = str_lines[0].lower()
		proportn = str_lines[1]
		
		if name not in map_ensembl_score:
			print (str_lines[0], file=outfile, sep="\t")
		else:
			pass

outfile.close ()
