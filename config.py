""" Script for configuring weighting given multiple output files gotten 
	from test.py. The functions are	designed to be called at the python 
	console. You should
	import numpy
	import config
	
	before calling any functions defined here. Usage for each function
	is described in detail under its declaration.
"""

import numpy as np

def get_file_data(filename):
	""" Reads text file outputted from running test.py.
		This file should represent a recording of music of similar
		style and genre. The less varied the style of music, the better.
		Hence, a good unit for recording is a song, or various songs
		in the same album. The longer the recording, the more data 
		can be operated on to give a more accurate configuration for
		weighting.
		
		filename is a string representing the name of the text file
		output by test.py.
	"""
	textfile = filename + ".txt"
	infile = open(textfile, "r")
	
	num_ints_on_line = 32	# number of integer values stored on a line
	sum_arr = np.array([0]*num_ints_on_line, dtype = np.float64)
	num_lines = 0
	for i, line in enumerate(infile):
		print "Calculating average, on line", str(i)
		str_list = line.split("\t")
		if str_list[-1] == "\n":
			del str_list[-1]
		flt_list = map(float, str_list)
		arr = np.array(flt_list, dtype = np.float64)
		sum_arr = np.add(sum_arr, arr)
		num_lines += 1
	average = np.divide(sum_arr, num_lines)
	
	infile.seek(0)
	tot_deviation = np.array([0.]*num_ints_on_line)
	for i, line in enumerate(infile):
		print "Calculating standard deviation, at line", str(i)
		str_list = line.split("\t")
		if str_list[-1] == "\n":
			del str_list[-1]
		flt_list = map(float, str_list)
		arr = np.array(flt_list, dtype = np.float64)
		deviation = np.abs(np.subtract(arr, average))
		
		tot_deviation = np.add(tot_deviation, deviation)
	variance = np.divide(tot_deviation, num_lines)
	std = np.sqrt(variance)
	
	infile.close()
	
	outname = filename + "_dat.txt"
	outfile = open(outname, "w")
	
	num_lines_string = "" + str(num_lines) + " \t <-- total number of" \
					   + " arrays in " + textfile + "\n"
	outfile.write(num_lines_string)
	
	for sumindex in range(len(sum_arr)):
		outfile.write(str(sum_arr[sumindex]))
		outfile.write("\t")
	outfile.write("<-- sum of values from all arrays in " + \
				  textfile + "\n")
	
	for avgindex in range(len(average)):
		outfile.write(str(average[avgindex])) 
		outfile.write("\t")
	outfile.write("<-- average values\n")	
	
	for devindex in range(len(tot_deviation)):
		outfile.write(str(tot_deviation[devindex])) 
		outfile.write("\t")
	outfile.write("<-- total deviations\n")	
	
	for stdindex in range(len(std)):
		outfile.write(str(std[stdindex])) 
		outfile.write("\t")
	outfile.write("<-- standard deviations\n")	
	
	outfile.close()
	return None
	 
	

