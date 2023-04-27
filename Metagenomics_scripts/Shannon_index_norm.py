#! /usr/bin/env python3
# This script will calculate the Shannon index for the output of Kraken 

import csv
import sys
import re
import numpy as np

input_tsv_file = sys.argv[1]
species_proportion = dict()
sum_proportn = 0

#output = input_tsv_file + '.micro_populatn'
with open (input_tsv_file,'r') as tsv:
	for lines in tsv:
		OTU = lines.split()[3]

		if "root" in lines:
			classified = float(lines.split()[0])	# Percentage of classified organisms

		if re.search('S$', OTU):
			proportn = float (lines.split()[0])
			if proportn > 0:
				sum_proportn = sum_proportn + proportn
				species = lines.split('\t')[5].strip()
				#print (species, proportn)
				species_proportion[species] = proportn


other_sp_proportn = classified - sum_proportn	# This gives the proportion of other species
species_proportion["Other"] = other_sp_proportn
microb_norm = classified - other_sp_proportn - species_proportion["Homo sapiens"] - species_proportion["Mycobacterium canettii"]
excluded_list = ["Other", "Homo sapiens", "Mycobacterium canettii"]
species_proportion.pop("Other")
species_proportion.pop("Homo sapiens")
species_proportion.pop("Mycobacterium canettii")

summation = 0
normalized_sp_proportion = dict()
for values in species_proportion:
	norm_val = ( species_proportion[values] * 1 ) / microb_norm
	normalized_sp_proportion[values] = norm_val
	#print (values, normalized_sp_proportion[values], sep="\t" )
	summation = summation  + (norm_val * (np.log(norm_val)))

shannon_index = -1 * (summation)
print (shannon_index)

# Sorting the array according to proportion
#sorted_norm_sp_proptn = dict (sorted(normalized_sp_proportion.items(), key = lambda kv: kv[1], reverse=True))

#outfile = open (output,'w')
#for vals in sorted_norm_sp_proptn:
#	if vals not in excluded_list:
#		print (vals,sorted_norm_sp_proptn[vals], file=outfile, sep="\t")

