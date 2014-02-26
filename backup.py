#!/usr/bin/env python

# Name     : googledrive-mysql-backup
# Author   : Gabriel C <shell.cooking@gmail.com>, cgFlamer @ github
# Requires : python
# Packages : os, time

import os
import config
import googledrive
import time

# Create backup file
backup_dbase = config.backup['dbase_pattern'] + time.strftime('%Y-%m-%d') + ".gz"
print "Create backup file of " + config.backup['mysql_dbase'] + " database into: " + backup_dbase
os.system("mysqldump -c -u " + config.backup['mysql_user'] + " -p" + config.backup['mysql_pass'] + " " + config.backup['mysql_dbse'] + "  | gzip -9 > " + config.backup['backup_path'] + backup_dbase)
print "Finished"

# Upload to google drive
from googledrive import uploadToGoogleDrive
uploadToGoogleDrive(config.backup['backup_path'] + backup_dbase, config.backup['google_user'], config.backup['google_pass'])