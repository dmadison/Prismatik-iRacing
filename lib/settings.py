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

import configparser
import lib.ir_utils as ir_utils
from lib.whitelist import irvar_whitelist as whitelist

def isFloat(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

def checkColorHex(color):
	# Check and remove prefixes
	if color[0:2] == '0x':
		color = color[2:]
	elif color[0] == 'x' or color[0] == '#':
		color = color[1:]

	if len(color) != 6:
		return

	try:
		color_rgb = []
		for i in range(0, 6, 2):
			color_rgb.append(int(color[i:i + 2], 16))
		return color_rgb
	except ValueError:
		return

class settings:
	def __init__(self, configfile):
		self.cfg = configfile + '.ini'
		self.ir = ir_utils.iracer()

		# Prismatik API Settings
		self.host = '127.0.0.1'
		self.port = 3636
		self.apiKey = None

		# iRacing API Settings
		self.apiVar = 'ShiftIndicatorPct'

		# Plugin Settings
		self.framerate = 60
		self.direction = 'symmetric'
		self.colors = [[0, 255, 0], [255, 255, 0], [255, 0, 0]]  # Green, Yellow, Red
		self.off_color = [0, 0, 0]
		self.smoothing = True
		self.filtering = 0.6

		self.parseConfig(self.cfg)

	def checkDirections(self, direction):
		directions = ['all', 'symmetric', 'clockwise', 'counter-clockwise']
		if direction in directions:
			return True
		return False

	def setFiltering(self, filter_in):
		if isFloat(filter_in):
			float_filter = float(filter_in)
			if float_filter >= 1.0:
				self.filtering = 1.0
			elif float_filter < 0.01:
				self.filtering = 0.01
			else:
				self.filtering = float_filter
			return

		if filter_in == 'none' or filter_in == 'off':
			self.filtering = 1.0
		elif filter_in == 'low':
			self.filtering = 0.6
		elif filter_in == 'medium' or filter_in == 'on':
			self.filtering = 0.4
		elif filter_in == 'high':
			self.filtering = 0.2

	def setColors(self, cfg_colors):
		colors_temp = cfg_colors.split(',')

		try:
			colors_new = []
			for color in colors_temp:
				color_rgb = checkColorHex(str.strip(color))
				if color_rgb is not None:
					colors_new.append(color_rgb)
			if len(colors_new) == len(colors_temp):  # All colors parsed successfully
				if len(colors_new) == 1:
					colors_new.insert(0, [0, 0, 0])  # Blank color to contrast with
				self.colors = colors_new
		except ValueError:
			pass

	def parseConfig(self, cfgName):
		config = configparser.ConfigParser()
		config.read(cfgName)

		try:
			self.host = config['Prismatik']['host']
			self.port = int(config['Prismatik']['port'])
			self.apiKey = config['Prismatik']['key']

			if config['iRacing']['var'] in whitelist:
				self.apiVar = config['iRacing']['var']

			framerate = int(config['User Settings']['fps'])
			if framerate <= 60:
				self.framerate = framerate

			if self.checkDirections(config['User Settings']['direction']):
				self.direction = config['User Settings']['direction']

			self.setColors(config['User Settings']['colors'])
			off_color = checkColorHex(config['User Settings']['off_color'])
			if off_color is not None:
				self.off_color = off_color

			self.smoothing = config.getboolean('User Settings', 'color_smoothing')
			self.setFiltering(config['User Settings']['data_filtering'])
		except (KeyError, ValueError):
			print("Error parsing cfg")
