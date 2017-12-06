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
from lib.utils import is_int, is_float, get_cfg_key, check_color_hex


class Settings:
	def __init__(self, configfile):
		self.cfg = configfile + '.ini'

		# Prismatik API Settings
		self.host = '127.0.0.1'
		self.port = 3636
		self.api_key = None

		# iRacing API Settings
		self.apiVar = 'ShiftIndicatorPct'
		self.var_min = 0.0
		self.var_max = 1.0

		# Plugin Settings
		self.framerate = 60
		self.direction = 'symmetric'
		self.colors = [[0, 255, 0], [255, 255, 0], [255, 0, 0]]  # Green, Yellow, Red
		self.off_color = [0, 0, 0]
		self.smoothing = True
		self.filtering = 0.6

		self.parse_config(self.cfg)

	def check_directions(self, direction):
		directions = ['all', 'symmetric', 'clockwise', 'counter-clockwise']
		if direction in directions:
			return True
		return False

	def set_filtering(self, filter_in):
		if is_float(filter_in):
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

	def set_colors(self, cfg_colors):
		colors_temp = cfg_colors.split(',')

		try:
			colors_new = []
			for color in colors_temp:
				color_rgb = check_color_hex(str.strip(color))
				if color_rgb is not None:
					colors_new.append(color_rgb)
			if len(colors_new) == len(colors_temp):  # All colors parsed successfully
				if len(colors_new) == 1:
					colors_new.insert(0, [0, 0, 0])  # Blank color to contrast with
				self.colors = colors_new
		except ValueError:
			pass

	def parse_config(self, cfgName):
		config = configparser.ConfigParser()
		config.read(cfgName)

		# Prismatik Settings
		config_var = get_cfg_key(config, 'Prismatik', 'host')
		self.host = config_var if config_var is not None else self.host

		config_var = get_cfg_key(config, 'Prismatik', 'port')
		if config_var is not None and is_int(config_var):
			self.port = int(config_var)

		config_var = get_cfg_key(config, 'Prismatik', 'key')
		self.api_key = config_var if config_var is not None else self.api_key

		# iRacing Settings
		config_var = get_cfg_key(config, 'iRacing', 'var')
		if config_var is not None and config_var in ir_utils.whitelist:
			self.apiVar = config_var

		config_var = get_cfg_key(config, 'iRacing', 'var_min')
		if config_var is not None and is_float(config_var):
			self.var_min = float(config_var)

		config_var = get_cfg_key(config, 'iRacing', 'var_max')
		if config_var is not None and is_float(config_var):
			self.var_max = float(config_var)

		# User Settings
		config_var = get_cfg_key(config, 'User Settings', 'fps')
		if config_var is not None and is_int(config_var):
			self.framerate = int(config_var) if int(config_var) <= 60 else 60

		config_var = get_cfg_key(config, 'User Settings', 'direction')
		if config_var is not None and self.check_directions(config_var):
			self.direction = config_var

		self.set_colors(get_cfg_key(config, 'User Settings', 'colors'))

		config_var = check_color_hex(get_cfg_key(config, 'User Settings', 'off_color'))
		self.off_color = config_var if config_var is not None else self.off_color

		try:
			self.smoothing = config.getboolean('User Settings', 'color_smoothing')
		except KeyError:
			print("Error parsing config:", "User Settings", "color_smoothing")

		config_var = get_cfg_key(config, 'User Settings', 'data_filtering')
		if config_var is not None:
			self.set_filtering(config_var)
