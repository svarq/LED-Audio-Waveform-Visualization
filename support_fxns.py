# Support functions for data manipulations
import numpy as np
from struct import unpack

# Define constants
tot_frequency = 20000

# The following functions are for the audio spectrum waveform visualisation
def piff(frequency, chunk):
	""" Power Index For Frequency:
	
		power is an array used below in fxn calculate_levels.
		It contains the values corresponding to the relative
		amplitude of the audio at certain frequencies.
		Assuming stream / microphone records from 
		0 - 20000 Hz, this function returns the index of array power 
		corresponding to a certain frequency, with results 
		spread out between the 0th index and the last index of power. 
	"""
	ratio = float(frequency) / tot_frequency
	num_indices = chunk/2
	index = ratio*num_indices
	return int(index)
   
def calculate_levels(zero_matrix, data, chunk, sample_rate):
#    weighting = [1,   2,   2,   2,   2,   1,   1,   1,   1,   1, 
#                 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
#                 1,   1,   1,   10,  10,  10,  8,  16,  16,  80, 
#                 160, 320]
    matrix = zero_matrix
    # Convert raw data (ASCII string) to numpy array of length chunk/2 +1
    data = unpack("%dH"%(len(data)/2),data)
    data = np.array(data, dtype='h')
    # Apply FFT - real data
    fourier=np.fft.rfft(data)
    # Remove last element in array to make it the same size as chunk/2
    fourier=np.delete(fourier,len(fourier)-1)
    # Find average 'amplitude' for specific frequency ranges in Hz
    power = np.abs(fourier)
    
    length = len(matrix)
    freq_step = tot_frequency/length
    for iii in range(length):
		freq1 = iii * freq_step
		freq2 = (iii + 1) * freq_step
		ind1 = piff(freq1, chunk)
		ind2 =  piff(freq2, chunk)
		matrix[iii] = int(np.mean(power[ind1: ind2]))
    
#    print matrix
    # Tidy up column values for the LED matrix
#    matrix=np.divide(np.multiply(matrix, weighting), 60000)
    # Set floor at 0 and ceiling at 32 for LED matrix
#    matrix=matrix.clip(0,32)
    return matrix
