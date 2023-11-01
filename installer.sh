#! /bin/bash
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

# Variables
homeDir="/home/pi/Oled"
serviceFile="/etc/systemd/system/oledinfo.service"
userRunning=`whoami`

# Common functions
homeDirectory() {
	mkdir -p $homeDir
	if [[ $? -eq 0 ]]; then
		echo -ne " --> OK"
	else
		echo -ne " --> ERROR, can't create the folder... Exiting..."
		exit 1
	fi
}
checkAction(){
if [[ $? -eq 0 ]]; then
	echo -ne " --> OK"
else
	echo -ne " --> ERROR. Something was wrong. Exiting..."
	exit 1
fi
}

# Starting the installator
echo "Wellcome to the Oled Information display installation"
echo " "
echo "------------------------------------------------------"

# Checking if the installator is running from root user
if [[ $userRunning != "root" ]]; then
	echo "Please, run this script with the root user."
	exit 1
fi

# checking if pi user exist (The home of this user is used to put the main scripts)
echo -ne "Checking if pi user exist"
checkUser=`id pi`
if [[ $checkUser == *"no such user"* ]]; then
	echo -ne " --> Oops, the user doesnt exists... Exiting..."
	exit 1
else
	echo -ne " --> Perfect, the user is here! Continuing..."
fi
echo " "
# Checking the internet connection (needed to install the dependencies with apt and pip3 install)
echo -ne "Checkig if there is an internet connection to install the dependencies..."
if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
	echo -ne " --> OK"
else
	echo -ne " --> ERROR. Please connect the Raspberry to the internet and run the installer again"
	exit 1
fi
echo " "
# Enabling I2C protocol
echo -ne "Enabling the I2C protocol in the GPIO of the Raspberry"
raspi-config nonint do_i2c 0
checkAction
echo " "
# Installing dependencies from apt
echo -ne "Installing dependencies..."
apt-get update && apt-get install python3 python3-pip -y -q
checkAction
echo " "
# Installing python3 libraries with pip3 install
echo -ne "Installing python3 libraries"
pip3 install pillow adafruit-circuitpython-ssd1306
checkAction
echo " "
# Creating the main directory of the service in the pi's home directory
echo -ne "Creating the directory $homeDir"
if [[ ! -d  $homeDir ]]; then
	homeDirectory
else
	echo -ne " --> The directory exists, so it will be deleted to continue the installation"
	echo "OK? (Write [ok|OK|Ok] or [no|NO|No])"
	read answer1
	if [[ $answer1 == "no" || $answer1 == "NO" || $answer1 == "No" ]]; then
		echo "Exiting..."
		exit 0
	elif [[ $answer1 == "ok" || $answer1 == "OK" || $answer1 == "Ok" ]]; then
		echo -ne "Deleting the folder..."
		rm -rf $homeDir
		checkAction
		homeDirectory
	fi
fi
echo " "
# Copying the main service files into the recent created directory
echo -ne "Putting the files in their place..."
cp Oled_info.py $homeDir/
cp Oled_info_stop.py $homeDir/
# Creating the systemd service file
touch $serviceFile
cat<<EOF>$serviceFile
[Unit]
Description=Oled information display
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/pi/Oled/Oled_info.py
ExecStop=/usr/bin/python3 /home/pi/Oled/Oled_info_stop.py
StartLimitBurst=0
[Install]
WantedBy=multi-user.target
EOF

if [[ $? -eq 0 && -f "$homeDir/Oled_info.py" && -f "$homeDir/Oled_info_stop.py" ]]; then
	echo -ne " --> OK"
else
	echo -ne " --> ERROR. Something was wrong. Exiting..."
	exit 1
fi
echo " "
# Changing permissions of the main service files to allow everyone everything (can be used 711)
echo -ne "Changing permissions on files"
chmod 777 "$homeDir/Oled_info.py" 
chmod 777 "$homeDir/Oled_info_stop.py"
checkAction
echo " "
# Reloading services to add the new one to the systemd list
echo -ne "Adding service to the system service database..."
systemctl daemon-reload
checkAction
echo " "
# Enabling the service to start it on every device boot
echo -ne "Enabling service..."
systemctl enable oledinfo.service
checkAction
echo " "
# Starting service
echo -ne "Starting service..."
systemctl start oledinfo.service
checkAction
echo " "
echo "In a few seconds, you should see the information on the Oled screen (If you have it connected properly)"
echo "-------------------------------------------------------------------------------------------------------------"
echo " "
echo "Installation Finished. Enjoy!"
