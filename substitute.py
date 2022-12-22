#! /usr/bin/env python3
# This script will substitute values in the excel file and write a output_temp.xlsx

import pandas as pd
import sys
import openpyxl

# Original xlsx file
input_xlsx_file = sys.argv[1]

xl_file = pd.read_excel(input_xlsx_file, sheet_name=None)
with pd.ExcelWriter('output_temp.xlsx') as writer:
	for sheet_names in xl_file.keys():
		df = pd.read_excel(input_xlsx_file, sheet_name=sheet_names)
		df.fillna(value= -1 , inplace=True)

		if 'VAF' in df:
			df["VAF"] = df["VAF"].astype(str).str.rstrip("%").astype(float)

		df = df.rename(columns={"VAF":"VAF (%)"})
		if 'PopFreqMax' in df:
			df["PopFreqMax"] = df["PopFreqMax"].astype(str).astype(float)

		if 'ALT_COUNT' in df:
			df["ALT_COUNT"] = df["ALT_COUNT"].astype(str).astype(int)

		df.to_excel(writer, sheet_name=sheet_names, index=False)
