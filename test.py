# Script for testing pyAudio, and giving output for configuring
# the weighting used in the support functions.

# Import PyAudio to get input stream from microphones, numpy for 
import pyaudio as pya
import numpy as np
import sys

# Import user-defined support functions for data manipulation
import support_fxns as fxns

# Setting up audio stream for sound capture
form = pya.paInt16
no_channels = 1
sample_rate = 44100
chunk = 4096
input_host_api = pya.paALSA

p = pya.PyAudio()
stream = p.open(format = form,
                channels = no_channels,
                rate = sample_rate,
                input = True,
                frames_per_buffer = chunk,
                input_device_index = 2)

# Spectrum Loop
zero_matrix = [0]*32
# output = open("Thundercat - A Fan's Mail (Tron Song Suite II)", "w")
while 1:
    try:
        # Get microphone data from stream
        data = stream.read(chunk, exception_on_overflow = False)
        matrix = fxns.calculate_levels(zero_matrix, data, chunk, sample_rate)
        print matrix
#        for iii in range(len(matrix)):
#            output.write(str(matrix[iii]))
#            output.write("\t")
#        output.write("\n")
    except KeyboardInterrupt:
        print("Ctrl-C Terminating...")
        stream.stop_stream()
        stream.close()
        p.terminate()
#        output.close()
        sys.exit(1)
    except Exception, e:
        print(e)
        print("ERROR Terminating...")
        stream.stop_stream()
        stream.close()
        p.terminate()
#        output.close()
        sys.exit(1)
