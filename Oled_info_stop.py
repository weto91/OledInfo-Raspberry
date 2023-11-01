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
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import adafruit_ssd1306
import time
import subprocess

# Initializing the OLED Screen in I2C Protocol.
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clearing the Display:
disp.fill(0)
disp.show()




