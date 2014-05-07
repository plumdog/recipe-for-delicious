#!/bin/bash

# Echo a message and exit
function error() {
	echo $1;
	exit 1;
}


virtualenv --python=python3.4 . || error "Unable to create virtualenv."
./bin/pip install -r dependencies.txt || error "Unable to install pip dependencies."
mysql -u root -p < mysql_init.sql || "Unable to create MySQL database and user.
