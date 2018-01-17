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

# This file is a release assembler that gathers the necessary build files for release and modifies the
# configuration files to point to the executable.
#
# !! Note that this MUST be run from within the src\build folder or the file paths won't resolve correctly. !!
#

import os
import shutil
import zipfile

build_name = 'Prismatik-iRacing'

# Set up common source and destination directories
current_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))
temp_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'release-temp'))
temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'release-temp', build_name))

# Check that the script is in the right folder
file_check = current_dir[len(root_dir):]
expected_directory = "\src\\build"

if file_check != expected_directory:
	raise UserWarning("Error: script not running from expected directory!")
else:
	print("Script running from expected directory")


# Copy helper class
class CopyPath:
	paths = []

	def __init__(self, source, destination, isdir=False):
		self.source = os.path.join(root_dir, source)
		self.destination = os.path.join(temp_dir, destination)
		self.directory = isdir
		self.paths.append(self)

	def copy(self):
		if self.directory:
			shutil.copytree(self.source, self.destination)
		else:
			shutil.copyfile(self.source, self.destination)

	def exists(self):
		if self.directory:
			return os.path.isdir(self.source)
		else:
			return os.path.isfile(self.source)


# Create copy objects with source and destination paths
dist = CopyPath(os.path.join('src', 'dist', build_name), 'dist', True)
icon = CopyPath(os.path.join('icons', 'icon.png'), os.path.join('dist', 'icon.png'))
presets = CopyPath('presets', 'presets', True)
user_config = CopyPath(os.path.join('src', 'cfg.ini'), 'cfg.ini')
plugin_config = CopyPath('Prismatik-iRacing-source.ini', build_name + '.ini')

# Check existence of all required files
for item in CopyPath.paths:
	print("Checking existence of", item.source)
	if not item.exists():
		raise UserWarning("Error! Path {} is missing".format(item.source))

# Create temporary directory
if not os.path.isdir(temp_root):
	print("Creating temporary folder...")
	os.mkdir(temp_root)
	os.mkdir(temp_dir)
else:
	raise UserWarning("Error! Temporary folder already exists! Remove it before continuing")

# Just a little hype :)
print(" ----- All systems go. LET'S DO IT!")

# Copy build
dist.copy()
print("Copied application files...")

# Copy configurations
user_config.copy()
print("Copied cfg.ini...")
presets.copy()
print("Copied presets folder...")
os.remove(os.path.join(presets.destination, "presets.md"))
print("Removed preset markdown file...")

# Modify and write new plugin configuration
f = open(plugin_config.source, 'r')
line_list = f.readlines()
f.close()

version_num = ""
with open(plugin_config.destination, 'w') as f_new:
	for line_num, line in enumerate(line_list):
		if line == "[Main]\n":
			line_list[line_num + 1] = "Name=iRacing Integration" + '\n'
			line_list[line_num + 2] = "Execute=dist/" + build_name + ".exe" + '\n'
			line_list[line_num + 3] = "Icon=dist/icon.png" + '\n'
		if "Version=" in line:
			version_num = line.split('=', 1)[1].rstrip()  # Pull out version number for zip title
		f_new.write(line)
f_new.close()
print("Copied and modified " + build_name + ".ini")

# Copy icon image
icon.copy()
print("Copied plugin icon...")


# Zip files for distribution
def zip(src, dst, name):
	zip_path = os.path.abspath(os.path.join(dst, name + ".zip"))
	zf = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
	abs_src = os.path.abspath(src)
	for dirname, subdirs, files in os.walk(abs_src):
		for filename in files:
			absname = os.path.abspath(os.path.join(dirname, filename))
			arcname = absname[len(abs_src) + 1:]
			print('Zipping %s as %s' % (os.path.join(dirname, filename),
										arcname))
			zf.write(absname, arcname)
	zf.close()


zip_name = build_name + '-' + version_num + '-' + "Plugin"
zip(temp_root, current_dir, zip_name)

# Clean up
print("Removing temporary files...")
shutil.rmtree(temp_root)

# Success!
print(" -----")
print("Release successfully created!")
