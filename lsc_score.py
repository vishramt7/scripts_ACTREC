#! /usr/bin/env python3

import sys

sample_list=sys.argv[1]		# List of samples from sample_list1
gene_weights = sys.argv[2]	# File containing ensembl id, gene names and their weights
folder_path = sys.argv[3]	# The Folder path which has the sample folders 
ABL_ensid = "ENSG00000097007"	# Ensembl id of ABL1 gene used as a normalization factor
outfile = "lsc_score.dat"

ensid_genes_map = dict()	# Dictionary for mapping ensembl id to gene names
ensid_weights = dict()		# Dictionary for mapping ensembl id to weights

output_file = open (outfile,'w')
with open (gene_weights, 'r') as weights_file:
	for gene_weights in weights_file:
		gene_weights_list = gene_weights.split()
		ensembl_id = gene_weights_list[0]
		gene_name = gene_weights_list[1]
		weights = float (gene_weights_list[2])
		ensid_genes_map[ensembl_id] = gene_name
		ensid_weights[ensembl_id] = weights

with open (sample_list,'r') as infile:
	for samples in infile:
		file_path = folder_path + '/' +''.join(samples.rstrip()) + '/' + ''.join(samples.rstrip()) + '.' + ''.join("subset.rawcounts_abl1.sorted.txt")
		output = folder_path + '/' +''.join(samples.rstrip()) + '/' + ''.join(samples.rstrip()) + '.' + ''.join("norm_expr.txt")
		outfile = open (output,'w')
		LSC_score = 0
		#print (file_path)
		with open (file_path, 'r') as sample_file:
			for expression_values in sample_file:
				samp_ensembl_id = expression_values.split()[0]
				expression = float(expression_values.split()[1])
				if ABL_ensid in samp_ensembl_id:		# Ensembl id for ABL
					ABL_expr = expression
					#print (samp_ensembl_id,"abl found", samples)
			
		with open (file_path, 'r') as sample_file:
			for expression_values in sample_file:
				samp_ensembl_id = expression_values.split()[0]
				expression = float (expression_values.split()[1])
				if ABL_ensid not in samp_ensembl_id and samp_ensembl_id in ensid_genes_map:	# Fetch ids other than ABL
					norm_expression = expression / ABL_expr
					product = norm_expression * ensid_weights[samp_ensembl_id]
					LSC_score = LSC_score + product
					print (samp_ensembl_id,norm_expression, file=outfile, sep="\t")
		outfile.close()
		print (samples.rstrip(), LSC_score, file=output_file, sep="\t")
