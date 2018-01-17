#
# Project     Prismatik - iRacing Plugin
# @author     David Madison
# @link       github.com/dmadison/Prismatik-iRacing
# @license    GPLv3 - Copyright (c) 2017 David Madison
#
# This file is part of the Prismatik - iRacing Plugin.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# This file is a script to change the version number throughout the repository:
# 	Prismatik-iRacing-source.ini - Plugin config
#   src\build\version.py - Windows executable information
#
# !! Note that this MUST be run from within the src\build folder or the file paths won't resolve correctly. !!
#

import os

# Set filenames
plugin_config_name = "Prismatik-iRacing-source.ini"
version_file_name = "version.py"

# Set up common paths
current_dir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

# Check that the script is in the right folder
file_check = current_dir[len(root_dir):]
expected_directory = "\src\\build"

if file_check != expected_directory:
	raise UserWarning("Error: script not running from expected directory!")

# Set up file paths
plugin_config = os.path.join(root_dir, plugin_config_name)
version_file = os.path.join(current_dir, version_file_name)

print("Prismatik-iRacing Plugin: Version Update Script")
print("----------")


def is_int(x):
	try:
		int(x)
		return True
	except ValueError:
		return False


version_major = ''
version_minor = ''
version_patch = ''

# Get new version number from user
valid_version = False
while not valid_version:
	version_major = input("Major #? ")
	version_minor = input("Minor #? ")
	version_patch = input("Patch #? ")

	valid_version = is_int(version_major) and is_int(version_minor) and is_int(version_patch)
	if valid_version:
		user_confirm = input("You inputted {}.{}.{}. Is that correct? (y/n) ".format(
			version_major, version_minor, version_patch))
		if user_confirm is not "y":
			print("Well get it right next time! <_<")
			valid_version = False
	else:
		print("That is not a valid version number.")

print("Version number looks good, let's do some stuff!")
print("-----")

version_3p = version_major + '.' + version_minor + '.' + version_patch
version_4p = version_3p + ".0"
version_tuple = '(' + version_major + ", " + version_minor + ", " + version_patch + ", " + "0)"

# Modify and write new plugin configuration
f = open(plugin_config, 'r')
line_list = f.readlines()
f.close()

with open(plugin_config, 'w') as f_new:
	for line in line_list:
		if "Version=" in line:
			line = "Version=" + version_3p + '\n'
		f_new.write(line)
f_new.close()
print("Updated version number in " + plugin_config_name)

# Modify and write new version file
f = open(version_file, 'r')
line_list = f.readlines()
f.close()

with open(version_file, 'w') as f_new:
	for line in line_list:
		if "filevers" in line or "prodvers" in line:
			line = line.split('=')[0] + '=' + version_tuple + ',' + '\n'
		elif "FileVersion" in line:
			line = line.split(',')[0] + ", u'" + version_4p + "')," + '\n'
		elif "ProductVersion" in line:
			line = line.split(',')[0] + ", u'" + version_4p + "')])" + '\n'
		f_new.write(line)
f_new.close()
print("Updated version number in " + version_file_name)

# Success!
print("-----")
print("Version change successful! Updated files to " + version_3p)
