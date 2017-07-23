# Main script to be executed for running visualizations for a 32x32
# RGB LED Matrix

# Import for making bibliopixel.LEDMatrix class for main matrix manipulations
from bibliopixel import *
import bibliopixel.colors as colors
from ada_matrix import DriverAdaMatrix
from rgbmatrix import Adafruit_RGBmatrix as ada

# Import PyAudio for audio capture data manipulation top be used for main
# matrix manipulations 
import pyaudio as pya

# Import user-defined support functions for data manipulation
import support_fxns as fxns
import numpy as np
import sys

# Make bibliopixel.LEDMatrix class object led
driver = DriverAdaMatrix(rows = 32, chain = 1)
driver.SetPWMBits(1)
led = LEDMatrix(driver, 32, 32, rotation = MatrixRotation.ROTATE_270, serpentine = False)

# Define a few colors. The color object is a tuple containing rgb values in the
# form (r,g,b)
r = colors.Red
g = colors.Green
b = colors.Blue

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
spectrum = [b]*15 + [g]*10 + [r]*7
zero_matrix = [0]*32
while 1:
    try:
        # Get microphone data
        data = stream.read(chunk, exception_on_overflow = False)
        matrix = fxns.calculate_levels(zero_matrix, data, chunk, sample_rate)

        led.all_off()
        for y in range(32):
            for x in range(matrix[y]):
                led.set(x, y, spectrum[x])
        led.update()
    except KeyboardInterrupt:
        print("Ctrl-C Terminating...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(1)
    except Exception, e:
        print(e)
        print("ERROR Terminating...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(1)
