# LED Audio Waveform Visualization
This is code developed for use with a Raspberry Pi in tandem with a 
microphone and a 32 x 32 RGB LED Matrix. Audio is recorded in real time,
and the recorded data is used to manipulate the input to the matrix from
the Pi. 
## Getting Started
In this section, I will summarize each file and directory in this 
repository, describe what technical equipment was used for the 
development of this code, what library dependencies the scripts
have.
### File & Directory Short Descriptions
spectrum.py - the main script, which records and manipulates sound data
			  and sends manipulated data to the matrix.
			  
support_fxns.py - used by spectrum.py and test.py to manipulate data.
				  spectrum.py can be considered as the brains of the
				  project, while support_fxns.py as the engine that 
				  provides the main data manipulation tools.
				  
test.py - 
				  
				  
