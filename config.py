""" Script for configuring weighting given multiple output files gotten 
	from test.py. The functions are	designed to be called at the python 
	console. You should
	import numpy
	import config
	
	before calling any functions defined here. Usage for each function
	is described in detail under its declaration.
"""

import numpy as np
from sys import argv
from sys import exit

def get_file_data(inputfile, outputfile):
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
    infile = open(inputfile, "r")

    num_ints_on_line = 32	# number of integer values stored on a line
    sum_arr = np.array([0]*num_ints_on_line, dtype = np.float64)
    num_lines = 0
    print "Calculating average."
    for i, line in enumerate(infile):
        if (i+1) % 1000 == 0:
            print "At line", str(i+1)
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
    print "Calculating standard deviation."
    for i, line in enumerate(infile):
        if (i+1) % 1000 == 0:
            print "At line", str(i+1)
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
	
    outfile = open(outputfile, "w")
	
    num_lines_string = "" + str(num_lines) + " \t <-- total number of" \
					   + " arrays in " + inputfile + "\n"
    outfile.write(num_lines_string)
	
    for sumindex in range(len(sum_arr)):
        outfile.write(str(sum_arr[sumindex]))
        outfile.write("\t")
    outfile.write("<-- sum of values from all arrays in " + \
				  inputfile + "\n")
	
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
	 
def get_mult_file_data(file_list):
    num_ints_on_line = 32
    num_lines = 0
    sum_arr = np.array([0]*32, dtype=np.float64)
    tot_deviation = np.array([0]*32, dtype=np.float64)

    for file in file_list:
        print "Working on file", file
        infile = open(file, "r")                

        # for loop designed with knowledge of formatting of input text files
        for i, line in enumerate(infile):
            str_list = line.split("\t")
            
            if i == 0:
                num_lines_file = int(str_list[0])
                num_lines += num_lines_file

            elif i == 1:
                for j in range(num_ints_on_line):
                    sum_arr[j] += float(str_list[j])

            elif i == 3:
                for j in range(num_ints_on_line):
                    tot_deviation[j] += float(str_list[j])
            
            else:
                continue

        infile.close()

    average = np.divide(sum_arr, num_lines)
    variance = np.divide(tot_deviation, num_lines)
    std = np.sqrt(variance)

    outfile = open("config.txt", "w")
    
    num_lines_string = "" + str(num_lines) + " \t <-- total number of " + \
                       "arrays in input data files.\n"
    outfile.write(num_lines_string)
	
    for sumindex in range(len(sum_arr)):
        outfile.write(str(sum_arr[sumindex]))
        outfile.write("\t")
    outfile.write("<-- sum of values from all arrays in " + \
                  "input data files.  \n")
	
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


if argv[1] == "filedata":
    if len(argv) != 4:
        exit("Incorrect number of arguments, try:\n" + \
             "python config.py filedata inputfile outputfile")
    # To add: error checking for whether inputfile and outputfile end in .txt
    get_file_data(argv[2], argv[3])

elif argv[1] == "multfiledata":
    if len(argv) < 4:
        exit("Incorrect number of arguments, try:\n" + \
             "python config.py multfiledata inputfiles[...]")
    file_list = []
    for index in range(len(argv)):
        if index < 2:
            continue
        # To add: error checking for whether any inputfiles end in .txt
        file_list.append(argv[index])
    get_mult_file_data(file_list)
    
else:
    exit("Use config.py with compatible data text files from test.py or config.py using either:\n\n" + \
         "python config.py filedata inputfile outputfile" + \
         "\n\tto produce an output text file with statistical data for a single" + \
         "\n\trecording data text file (inputfile) produced from test.py.\n\n" + \
         "python config.py multfiledata inputfiles[...]" + \
         "\n\tto produce an output file giving statistical data on a set of files" + \
         "\n\toutput by calling \tconfig.py filedata." + \
         "\n\tinputfiles[...] corresponds to input files as arguments separated by a space.\n") 
