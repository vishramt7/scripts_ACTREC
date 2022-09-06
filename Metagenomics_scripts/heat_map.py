#! /usr/bin/env python3
# This script will make a heatmap for a given set of organisms from the proportion data

import sys
import re
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

input_tsv_file = sys.argv[1]
directory_path = "./"
ext_of_files = ".populatn"

organisms = dict()
organisms_list = list()
with open (input_tsv_file,'r') as tsv:
	for lines in tsv:
		name = lines.split('\t')[0].strip()
		organisms[name] = 0
		organisms_list.append(name)

sample_name_list = list()
org_list_list = list()

for i in range(len(organisms_list)):		# Making a list of empty lists
	org_list_list.append([])

count = 0
for files in os.listdir(directory_path):	# Looping over all the files with a given extension
	if files.endswith(ext_of_files):
		sample_name = files.split('_')[0]	# Extracting the sample name from file name
		sample_name_list.append(sample_name)

		for i in range(len(organisms_list)):
			org_list_list[i].append(0) 

		with open (files, 'r') as infile:
			for inlines in infile:
				name = inlines.split('\t')[0]
				pop_fractn = float (inlines.split('\t')[1])
				
				if name in organisms_list:
					indx = organisms_list.index(name)
					org_list_list[indx][count] = pop_fractn
				else:
					pass
					
		count = count + 1
	else:
		pass

#print (sample_name_list, len(organisms_list), len(org_list_list[1]))
#print (org_list_list)
df = pd.DataFrame(org_list_list, columns = sample_name_list, index = organisms_list)
plt.imshow(df, cmap = "hot_r")
plt.colorbar(shrink=0.6)
plt.clim(0, 1);
plt.xticks(range(len(sample_name_list)), df.columns, rotation = 90)
plt.yticks(range(len(organisms_list)), df.index)
plt.savefig("out_batch1.png", dpi=600, bbox_inches = 'tight', pad_inches = 0)
plt.close()
exit()
