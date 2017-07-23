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

def get_file_data(upper_bound_led, inputfile_list, outputfile):
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

    num_ints_on_line = 32	# number of integer values stored on a line in an inputfile
    
    print "Calculating average,"
    inputfile_list_str = ""
    num_lines = 0
    sum_arr = np.array([0]*num_ints_on_line, dtype = np.float64)
    for file in inputfile_list:
        print "Working on file", file
        inputfile_list_str += (file + ", ")
        infile = open(file, "r")
    
        for i, line in enumerate(infile):
            str_list = line.split("\t")
            if str_list[-1] == "\n":
                del str_list[-1]
            flt_list = map(float, str_list)
            val_arr = np.array(flt_list, dtype = np.float64)
            sum_arr = np.add(sum_arr, val_arr)
            num_lines += 1
        infile.close()
    average = np.divide(sum_arr, num_lines)

    print "Calculating standard deviation,"
    tot_dev = np.array([0]*num_ints_on_line, dtype = np.float64)
    for file in inputfile_list:
        print "Working on file", file
        infile = open(file, "r")
        for i, line in enumerate(infile):
            str_list = line.split("\t")
            if str_list[-1] == "\n":
                del str_list[-1]
            flt_list = map(float, str_list)
            arr = np.array(flt_list, dtype = np.float64)
            deviation = np.abs(np.subtract(arr, average))
            tot_dev = np.add(tot_dev, deviation)
        infile.close()

    variance = np.divide(tot_dev, num_lines)
    std = np.sqrt(variance)

    # producing weighting for use in spectrum.py
    upper_bound_data_arr = np.add(average, std)     # the "typical upper bound" of raw data values in audio stream
    max_upper_bound_data = np.amax(upper_bound_data_arr)
    common_divisor = int(max_upper_bound_data / upper_bound_led)
    sample = np.divide(upper_bound_data_arr, common_divisor)    # sample of typical matrix values to be multiplied by weighting to give upper_bound_led
    weighting = np.divide(upper_bound_led, sample)
    weighting = np.rint(weighting)
    weighting = np.array(weighting, dtype=np.int32)

    outfile = open(outputfile, "w")

    outfile.write("Input data files:\t" + inputfile_list_str + "\n")
            
    outfile.write("Total number of arrays -->\t" + str(num_lines) + "\n")

    outfile.write("Sum of values from all arrays -->\t")
    for sumindex in range(len(sum_arr)):
        outfile.write(str(sum_arr[sumindex]) + "\t")
    outfile.write("\n")

    outfile.write("Average values -->\t")
    for avgindex in range(len(average)):
        outfile.write(str(average[avgindex]) + "\t")
    outfile.write("\n")

    outfile.write("Total deviations -->\t")	
    for devindex in range(len(tot_dev)):
        outfile.write(str(tot_dev[devindex]) + "\t") 
    outfile.write("\n")

    outfile.write("Standard deviations -->\t")	
    for stdindex in range(len(std)):
        outfile.write(str(std[stdindex]) + "\t") 
    outfile.write("\n")

    outfile.write(("_" * 200) + "\nCONFIG VALUES:\n")

    outfile.write("LED \"typical\" upper bound -->\t" + str(upper_bound_led) + "\n")

    outfile.write("Common divisor -->\t" + str(common_divisor) + "\n")

    outfile.write("Weighting -->\t")
    for wtindex in range(len(weighting)):
        outfile.write(str(weighting[wtindex]) + "\t")

    outfile.close()
    return None


if len(argv) == 1:
    exit("python config.py LEDupperbound inputfiles[...] outputfile\n\n" + \
         "config.py outputs a text file, outputfile,\n" + \
         "with data from all inputfiles. Works for 1 or\n" + \
         "more entered raw data files produced from test.py.\n\n" + \
         "Note that inputfiles[...] means to enter all\n" + \
         "input text files produced from test.py,\n" + \
         "separated by whitespace.")

elif (len(argv)==1) and (len(argv)<=3):
    exit("Error: wrong number of arguments.\n\n" + \
         "For more info about config.py, type:\n\t" + \
         "python config.py")

elif(int(argv[1])<0) or (int(argv[1])>32):
    exit("Error: first agument (LEDupperbound) to python config.py\n" + \
         "should be an integer between 0-32.\n\n" + \
         "For more info about config.py, type:\n\t" + \
         "python config.py")

else:
    upper_bound_led = int(argv[1])
    inputfile_list = []
    outputfile = ""
    for index in range(2, len(argv)):
        file = argv[index]
        
        if file.endswith(".txt") == False:
            exit("Error: all files entered at commandline must\n" + \
                 "end in \".txt\".\n\n" + \
                 "For more info about config.py, type:\n\t" + \
                 "python config.py")
        
        if index == (len(argv)-1):
            outputfile = file
            continue

        inputfile_list.append(file)
    get_file_data(upper_bound_led, inputfile_list, outputfile)
