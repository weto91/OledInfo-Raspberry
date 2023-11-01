### Features
You can show the following information in a simple (and cheap) I2C 0,96inch OLED screen:
- CPU Temperature (Celsius)
- Free RAM Memory (Percentage)
- Used HDD (Percentage)
- Clock (HH:MM)

**Table of Contents**

[TOCM]

##Prerequisites
After the installation process, you need to meet a series of hardware and software requirements:
###Hardware requirements:
- Raspberry PI: Any model. Although this project has been tested on Raspberry PI Zero 2 W, Raspberry PI 3 and Raspberry PI 4.
- SSD1306: I2C (4 pin) 0,96inch 128x64 px OLED Display: You can buy it on Aliexpress, Amazon or Adafruit.
- MicroSD with sufficient space to alocate this project (3Mb).
- 4 cables to wire the screen to the GPIOs in the Raspberry PI.
###Software requirements:
- You need (obviously) the operative system installed. RaspiOS, Raspbian... the one you like the most, based on Raspbian.
- Need to be connected to the internet. The installer will install all the dependencies and will need an internet connection
- The user "pi" configured
- The user "root" available to run the installer (only works with root user)
##Hardware installation and wiring
You can follow the image below.

|  SSD1306  | Raspberry PI  |
| :------------: | :------------: |
|  VCC |  5V (can be on 3v3)  |
|  GND | GND  |
|  SCK |  SCK (GPIO3)  |
|  SDA | SDA (GPIO2)  |

<img src="https://github.com/weto91/OledInfo-Raspberry/blob/main/oled_wiring.jpg?raw=true" width="358" height="400">

##Installation process
The installation is so easy:
1. clone this repository in /tmp of your Raspberry Pi
`# git clone https://github.com/weto91/OledInfo-Raspberry /tmp`
2. Change permissions of the installer.sh file as root (700)
`# chmod 700 /tmp/OledInfo-Raspberry/installer.sh`
3. Run the installer
`# ./tmp/OledInfo-Raspberry/installer.sh`
4. Wait until the installation process finish and enjoy!

## Results
<img src="https://github.com/weto91/OledInfo-Raspberry/blob/main/IMG_3635.jpg?raw=true" width="358" height="400">

