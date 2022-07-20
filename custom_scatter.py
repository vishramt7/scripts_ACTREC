#!/usr/bin/env python3

from matplotlib import pyplot as plt
import re
import sys

chr_list_file = sys.argv[1]	# file containing information to be plotted
cnr_file = sys.argv[2]		# .cnr file 
cns_file = sys.argv[3]		# .cns file
outfile = sys.argv[4]		# Name of the output file

output_file = open (outfile,'w')
i = 0
pattern = re.compile("#")
with open (chr_list_file) as file_input:
	for lines in file_input:
		remove_hash = pattern.match(lines)
		if not remove_hash:
			columns = lines.split()
			i = i + 1
			no_of_subplots = len (columns[0].split(','))
			chr_start_stop_list = columns[0].split(',')
			band_list = columns[1].split(',')
			#print (chr_start_stop_list)
			#fig, axs = plt.subplots(nrows = 1, ncols = 2)
			for values in range(0, no_of_subplots):
				X_axis_list = list()
				Y_axis_list = list()
				weights_list = list()
				cns_log2_list = list()
				ci_lo_list = list ()
				ci_hi_list = list ()
				ci_chrstart_list = list ()
				ci_chrend_list = list ()
				chr_name = chr_start_stop_list[values].split(':')[0]
				chr_name = re.sub ("chr","", chr_name, flags = re.IGNORECASE)
				chr_name = re.sub ("X","x", chr_name, flags = re.IGNORECASE)
				chr_name = re.sub ("Y","y", chr_name, flags = re.IGNORECASE)
				start_val = int ((chr_start_stop_list[values].split(':')[1]).split('-')[0])
				stop_val = int ((chr_start_stop_list[values].split(':')[1]).split('-')[1])
				band_name = band_list[values]
				print (chr_name, start_val, stop_val,band_name)

				with open (cnr_file) as cnr_input_file:
					next (cnr_input_file)	# Avoiding the headers
					for cnr_lines in cnr_input_file:	
						cnr_chr = cnr_lines.split()[0]
						cnr_chr = re.sub ("chr","", cnr_chr, flags = re.IGNORECASE)
						cnr_chr = re.sub ("X","x", cnr_chr, flags = re.IGNORECASE)
						cnr_chr = re.sub ("Y","y", cnr_chr, flags = re.IGNORECASE)
						if cnr_chr == chr_name:
							cnr_start = int (cnr_lines.split()[1])
							cnr_end = int (cnr_lines.split()[2])
							if cnr_start >= start_val and cnr_end <= stop_val:
								x_val = int (( cnr_start  + cnr_end ) / 2)	
								log2 = float (cnr_lines.split()[5])
								weight = float (cnr_lines.split()[6]) * 50.0	# Increasing the size of points
								X_axis_list.append (x_val)
								Y_axis_list.append (log2)
								weights_list.append (weight)

							if cnr_end > stop_val:
								break

				with open (cns_file) as cns_input_file:
					next (cns_input_file)
					for cns_lines in cns_input_file:
						cns_chr = cns_lines.split()[0]
						cns_chr = re.sub ("chr","", cns_chr, flags = re.IGNORECASE)
						cns_chr = re.sub ("X","x", cns_chr, flags = re.IGNORECASE)
						cns_chr = re.sub ("Y","y", cns_chr, flags = re.IGNORECASE)
						if cns_chr == chr_name:
							cns_start = int (cns_lines.split()[1])
							cns_end = int (cns_lines.split()[2])
							if start_val >= cns_start and stop_val <= cns_end:
								print (cns_start, cns_end)
								cns_log2 = float (cns_lines.split()[4])
								cns_li = float (cns_lines.split()[8])
								cns_hi = float (cns_lines.split()[9])
								ci_chrstart_list.append (cns_start)
								ci_chrend_list.append (cns_end)
								ci_lo_list.append (cns_li)
								ci_hi_list.append (cns_hi)
								cns_log2_list.append (cns_log2)

			plt.figure()		
			plt.scatter (X_axis_list, Y_axis_list, s=weights_list, alpha=0.4, color='gray')	# Scatter plot of the data points
			plt.plot ([X_axis_list[0], X_axis_list[-1]], [0,0],'k')							# Plotting the x-axis
			for ci_line in range (0, len(ci_chrstart_list)):
				#print (ci_chrstart_list[ci_line], ci_chrend_list[ci_line], ci_lo_list[ci_line], ci_hi_list[ci_line])
				plt.plot ([ci_chrstart_list[ci_line], ci_chrend_list[ci_line]],[ cns_log2_list[ci_line], cns_log2_list[ci_line]], color='darkorange', linewidth=3, solid_capstyle='round')	

			lower = X_axis_list[0] - 100000		# Adding a buffer of 100000 for proper visualization
			upper = X_axis_list[-1] + 100000	
			plt.xlim (lower, upper)
			plt.xlabel('Position')
			plt.ylabel('Copy ratio (log2)')
			output = outfile + "_cnv_" + str(i) + '.png'
			plt.title(band_name)
			plt.savefig(output, format = 'png', dpi = 300, transparent=True, bbox_inches='tight',pad_inches = 0)
			print ( X_axis_list, Y_axis_list, file=output_file)
			# print (len(X_axis_list), len(Y_axis_list), len (weights_list))
			#	ax = axs[values]
			#	ax = cnvlib.do_scatter(cn, segments,show_range=chr_start_stop_list[values], title=band_list[values])
			#	print (values)
			#	print (chr_start_stop_list[values], band_list[values])

			#print (chr_start_stop, output)		
			#ax = cnvlib.do_scatter(cn, segments,show_range=chr_start_stop, window_width=100, title=band)
			#plt.title(band)
			#plt.rcParams["font.size"] = 9.0	
			#plt.savefig(output, format = 'png', dpi = 300, transparent=True, bbox_inches='tight',pad_inches = 0)
		else:
			continue	

