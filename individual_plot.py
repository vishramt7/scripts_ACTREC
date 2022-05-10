#!/usr/bin/env python3

from matplotlib import pyplot as plt
import cnvlib
import re
import sys

chr_list_file = sys.argv[1]		# file containing information to be plotted
cn = cnvlib.read(sys.argv[2])		# .cnr file 
segments = cnvlib.read(sys.argv[3])	# .cns file
outfile = sys.argv[4]			# Name of the output file

i = 0
pattern = re.compile("#")
with open (chr_list_file) as file_input:
	for lines in file_input:
		remove_hash = pattern.match(lines)
		if not remove_hash:
			columns = lines.split()
			chr_start_stop = columns[0]
			band = columns[1]
			i = i + 1
			output = outfile + "_cnv_" + str(i) + '.png'	
			print (chr_start_stop, output)		
			ax = cnvlib.do_scatter(cn, segments,show_range=chr_start_stop)
			plt.title(band)
			#plt.rcParams["font.size"] = 9.0	
			plt.savefig(output, format = 'png', dpi = 300, transparent=True, bbox_inches='tight',pad_inches = 0)
		else:
			continue	



