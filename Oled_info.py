#*
#* OledInfo-Raspberry - A service to display system information on a 0.96 inch I2C oled display on Raspberry PI
#*
#* Copyright (C) 2023 Álvaro Rubio
#*
#* This program is free software; you can redistribute it and/or
#* modify it under the terms of the GNU General Public License
#* as published by the Free Software Foundation; either version 2
#* of the License, or (at your option) any later version.
#*
#* This program is distributed in the hope that it will be useful,
#* but WITHOUT ANY WARRANTY; without even the implied warranty of
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#* GNU General Public License for more details.
#*
#* You should have received a copy of the GNU General Public License
#* along with this program; if not, write to the Free Software
#* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#*

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
import subprocess

# Variables
tempCPU = None
freeMem = None
diskUsage = None
timeCus = None
fontType = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" # you can change the font as you like, but take care with line 70, here you can change the Font size.

# Initializing the OLED Screen in I2C Protocol.
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clearing the Display on start:
disp.fill(0)
disp.show()


# Preparing the screen to show text in all space of the OLED Screen (128x64 pixels)
image = Image.new('1', (128, 64))
draw = ImageDraw.Draw(image)

def proc_run(command) :
	info = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
	return info.stdout.decode().strip()
def displayer(img) :
		disp.image(img)
		disp.show()
def rectangle_drawer(x1 ,x2, y1, y2 ):
	draw.rectangle(((x1,x2),(y1,y2)), fill="black")
def text_drawer(x,y, info,font):
	draw.text((x, y), info, font=font, fill=255)

# Loop to run the script non-stop
if __name__ == "__main__":
	while True:
		# CPU Temperature:
		resultCPUTemp = proc_run('vcgencmd measure_temp | egrep -o \'[0-9]*\.[0-9]*\'')
		textCPUShow = 'CPU Temp: %s ºC' % resultCPUTemp 
		
		# Free RAM Memory percent
		resultFreeMem = proc_run('free -m |head -n +2 | awk -F" " \'{print $4}\' | tail -n +2')
		resultTotMem = proc_run('free -m |head -n +2 | awk -F" " \'{print $2}\' | tail -n +2')
		resultTotMem = round(resultTotMem * 100 / resultFreeMem, 0)
		memoryPercent = str(resultTotMem) 
		textMEMShow = 'Free RAM  : %s' % memoryPercent
		
		# Disk usage percent
		resultUsaDisk = proc_run('df -h | grep "/dev/root" | awk -F" " \'{print $5}\'')
		textDISKShow = 'D. Usage   : %s' % resultUsaDisk
		
		# Clock with hours and minutes
		resultClock = proc_run('date +"%H:%M"')
		textClockShow = 'Clock         : %s' % resultClock

		# Preparing the font and font size
		font = ImageFont.truetype(fontType, 14)

		
		if resultCPUTemp != tempCPU:
			rectangle_drawer(80, 1 ,128, 16)
		if memoryPercent != freeMem:
			rectangle_drawer(80, 17 ,128, 32)
		if resultUsaDisk != diskUsage:
			rectangle_drawer(80, 33,128, 48)
		if resultClock != timeCus:
			rectangle_drawer(80, 49, 128, 64)

		displayer(image)

		# Writing the text (X pixel, Y pixel, text, font, Color: For monochromatic Oled screen, 255 is OK.)):
		text_drawer(0, 1, textCPUShow, font=font)
		text_drawer(0, 17, textMEMShow, font=font)
		text_drawer(0, 33, textDISKShow, font=font)
		text_drawer(0, 49, textClockShow, font=font)

		# Show the written text:
		displayer(image)
		
		# Copying the results to the main variables to compare it in the next loop
		tempCPU = resultCPUTemp
		freeMem = memoryPercent
		diskUsage = resultUsaDisk
		timeCus = resultClock
		# Timer to wait the next loop. 
		time.sleep(4) # You can change this number (seconds). > if you need the service to use fewer resources or < If you need the screen to refresh the information faster.
