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


# Loop to run the script non-stop
while True:
	# CPU Temperature:
	resultCPUTemp = subprocess.run('vcgencmd measure_temp | egrep -o \'[0-9]*\.[0-9]*\'', shell=True, stdout=subprocess.PIPE)
	textCPUShow = 'CPU Temp: ' + resultCPUTemp.stdout.decode().strip() + '°C'
    
    # Free RAM Memory percent
    resultFreeMem = subprocess.run('free -m |head -n +2 | awk -F" " \'{print $4}\' | tail -n +2', shell=True, stdout=subprocess.PIPE)
	resultTotMem = subprocess.run('free -m |head -n +2 | awk -F" " \'{print $2}\' | tail -n +2', shell=True, stdout=subprocess.PIPE)
	memoryPercent = int(resultFreeMem.stdout.decode().strip()) * 100 / int(resultTotMem.stdout.decode().strip())
    textMEMShow = 'Free RAM  : ' + str(round(memoryPercent, 0)) + '%'
    
    # Disk usage percent
    resultUsaDisk = subprocess.run('df -h | grep "/dev/root" | awk -F" " \'{print $5}\'', shell=True, stdout=subprocess.PIPE)
    textDISKShow = 'D. Usage   : ' + resultUsaDisk.stdout.decode().strip()
    
    # Clock with hours and minutes
	resultClock = subprocess.run('date +"%H:%M"', shell=True, stdout=subprocess.PIPE)
	textClockShow = 'Clock         : ' + resultClock.stdout.decode().strip()

	# Preparing the font and font size
	font = ImageFont.truetype(fontType, 14)

	
	if resultCPUTemp.stdout.decode().strip() != tempCPU:
		draw.rectangle(((80, 1), (128, 16)), fill="black")
	if str(round(memoryPercent, 0)) != freeMem:
		draw.rectangle(((80, 17), (128, 32)), fill="black")
	if resultUsaDisk.stdout.decode().strip() != diskUsage:
		draw.rectangle(((80, 33), (128, 48)), fill="black")
	if resultClock.stdout.decode().strip() != timeCus:
		draw.rectangle(((80, 49), (128, 64)), fill="black")

	disp.image(image)
	disp.show()
	# Writing the text (X pixel, Y pixel, text, font, Color: For monochromatic Oled screen, 255 is OK.)):
	draw.text((0, 1), textCPUShow, font=font, fill=255)
	draw.text((0, 17), textMEMShow, font=font, fill=255)
	draw.text((0, 33), textDISKShow, font=font, fill=255)
	draw.text((0, 49), textClockShow, font=font, fill=255)

	# Show the written text:
	disp.image(image)
	disp.show()
    
    # Copying the results to the main variables to compare it in the next loop
	tempCPU = resultCPUTemp.stdout.decode().strip()
	freeMem = str(round(memoryPercent, 0))
	diskUsage = resultUsaDisk.stdout.decode().strip()
	timeCus = resultClock.stdout.decode().strip()
    # Timer to wait the next loop. 
	time.sleep(4) # You can change this number (seconds). > if you need the service to use fewer resources or < If you need the screen to refresh the information faster.
