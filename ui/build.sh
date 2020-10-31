#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

if [ ! -f /usr/bin/setup_14.x ]
then
	echo "Node not installed. Initiating installation."
	curl -O https://rpm.nodesource.com/setup_14.x  
	if [ -f setup_14.x ]
	then
		mv setup_14.x /usr/bin/setup_14.x
		chmod 755 /usr/bin/setup_14.x
		echo "Running setup."
		/usr/bin/setup_14.x
		if [ $? -ne 0 ]
		then
			echo "Node setup unsuccessfull."
			exit 1
		fi
		echo "NodeJS RPM installation."
		yum install -y nodejs
		if [ $? -ne 0 ]
                then
                        echo "NodeJS RPM installation unsuccessfull."
                        exit 1
                fi
		echo "Installation complete."
	else
		if [ $? -ne 0 ]
                then
                        echo "Download setup unsuccessfull."
                        exit 1
                fi
	fi
else
	echo "NodeJS already installed."
fi
echo "Deleting previous builds."
rm -rf node_modules build
echo "Installing dependencies."
/usr/bin/npm install
if [ $? -ne 0 ]
then
	echo "Dependency installation failed."
fi
echo "Building application."
/usr/bin/npm run build
if [ $? -ne 0 ]
then
        echo "Build failed."
fi
