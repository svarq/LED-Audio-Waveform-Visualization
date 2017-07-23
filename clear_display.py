from bibliopixel import *
from ada_matrix import DriverAdaMatrix
from rgbmatrix import Adafruit_RGBmatrix as ada


driver = DriverAdaMatrix(rows = 32, chain = 1)
driver.SetPWMBits(1)
led = LEDMatrix(driver, 32, 32, rotation = MatrixRotation.ROTATE_270, serpentine = False)
led.all_off()
