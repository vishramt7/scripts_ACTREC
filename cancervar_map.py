#! /usr/bin/env python3
# This script takes the cancervar phred file and final.xlsx file as input,
# It writes a cancervar_temp.csv file as a temporary file
# It writes this temp file to the final.xlsx

import sys
import openpyxl
import pandas as pd
import csv
import re
import os

cancervar_file = sys.argv[1]	# cancervar phred file
excel_file = sys.argv[2]		# Final .xlsx file
temp_cancervar_file = "cancervar_temp.csv"
new_sheetname = "append_CancerVar"

map_evidence = dict()             # Dictionary for the marker occurence
map_ensembl_score = dict()
df = pd.read_csv(cancervar_file, delimiter = '\t')
for row_nums in df.index:
	chrom = df['#Chr'][row_nums]
	start = df['Start'][row_nums]
	end = df['End'][row_nums]
	ref = df['Ref'][row_nums]
	alt = df['Alt'][row_nums]
	evidence = str(df[' CancerVar: CancerVar and Evidence '][row_nums]).replace(',',' ')
	ensembl_score = str(df['ensemble_score'][row_nums]).replace(',',' ')

	if re.search('[a-zA-Z]', str(chrom)):
		chrom = re.sub ("chr","", chrom, flags = re.IGNORECASE)
		chrom = re.sub ("X","23", chrom, flags = re.IGNORECASE)
		chrom = re.sub ("Y","y", chrom, flags = re.IGNORECASE)

	id = str(chrom) + ':' +''.join(str(start)) + ':' +''.join(str(end)) + ':' +''.join(str(ref)) + ':' +''.join(str(alt))
	map_evidence[id] = evidence
	map_ensembl_score[id] = ensembl_score
	#print (df['#Chr'][row_nums], df['Start'][row_nums], df['End'][row_nums], df['Ref'][row_nums], df['Alt'][row_nums], evidence, ensembl_score,sep="\t")

outfile = open (temp_cancervar_file,'w')
xl_file = pd.read_excel(excel_file, sheet_name=None)
for sheet_names in xl_file.keys():
	df = pd.read_excel(excel_file, sheet_name=sheet_names)
	df.fillna(value= -1 , inplace=True)
	if 'append_final_concat' in sheet_names:
		print (str(df.columns.tolist())[1:-1], "CancerVar evidence", "ensembl score", file=outfile, sep=',')
		for rows in df.index:
			chrom_xl = df['Chr'][rows]
			start_xl = df['Start'][rows]
			end_xl = df['End'][rows]
			ref_xl = df['Ref'][rows]
			alt_xl = df['Alt'][rows]
			if re.search('[a-zA-Z]', str(chrom_xl)):
				chrom_xl = re.sub ("chr","", chrom_xl, flags = re.IGNORECASE)
				chrom_xl = re.sub ("X","23", chrom_xl, flags = re.IGNORECASE)
				chrom_xl = re.sub ("Y","y", chrom_xl, flags = re.IGNORECASE)

			id_xl = str(chrom_xl) + ':' +''.join(str(start_xl)) + ':' +''.join(str(end_xl)) + ':' +''.join(str(ref_xl)) + ':' +''.join(str(alt_xl))
			if id_xl in map_evidence:
				print (str(df.loc[rows, :].values.tolist())[1:-1],map_evidence[id_xl], map_ensembl_score[id_xl], file=outfile,sep=',')
				#print (df.columns.tolist()[1:-1],map_evidence[id_xl], map_ensembl_score[id_xl], sep=',')
			else:
				print (str(df.loc[rows, :].values.tolist())[1:-1],"-","-", file=outfile,sep=',')
				#print (df.columns.tolist()[1:-1],"-","-", sep=',')


wb = openpyxl.load_workbook(excel_file)
if os.path.getsize(temp_cancervar_file) != 0:
	worksheet = wb.create_sheet(new_sheetname)
	#read_csv = csv.reader(open(temp_cancervar_file, 'r', encoding='utf-8'), delimiter=',', error_bad_lines=True)
	#for rows in read_csv:
	#	worksheet.append(rows)

	#df_check = pd.read_csv(temp_cancervar_file, error_bad_lines=True)
	#df.to_excel(wb,sheet_name=, index=False)
	#for rows in df_check.index:
		#worksheet.append(tuple(str(df_check.loc[rows, :].values.tolist())[1:-1]))

	with open (temp_cancervar_file,'r') as csv_file:
		csv_handle = csv.reader(csv_file)
		for lines in csv_handle:
			print (lines)
			worksheet.append(tuple(lines))

wb.save(excel_file)

#df2 = pd.read_csv(temp_cancervar_file)
#with pd.ExcelWriter(excel_file, mode='rw') as writer:
#	df2.to_excel(excel_file, sheet_name=new_sheetname, index=False, header=True)
