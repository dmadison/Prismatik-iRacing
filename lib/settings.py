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
import os
import lib.ir_utils as ir_utils
from lib.utils import is_int, is_float, check_color_hex


class Settings:
	def __init__(self, configfile):
		# Prismatik API Settings
		self.host = '127.0.0.1'
		self.port = 3636
		self.api_key = None

		# iRacing API Settings
		self.api_var = 'ShiftLight'
		self.var_min = 0.0
		self.var_max = 1.0

		# Plugin Settings
		self.framerate = 60
		self.pattern = 'symmetric'
		self.colors = [[0, 255, 0], [255, 255, 0], [255, 0, 0]]  # Green, Yellow, Red
		self.off_color = [0, 0, 0]
		self.single_color = False
		self.bidirectional_color = False
		self.blink_rate = 2.5  # in Hertz
		self.smoothing = True
		self.filtering = 0.6

		# Debug Settings
		self.debug_print = False

		# Load Defaults
		self.__preset_applied = False
		self.parse_config('presets\defaults.ini')

		# Load User Settings
		self.cfg = configfile + '.ini'
		self.parse_config(self.cfg)

	def check_patterns(self, pattern):
		patterns = ['all', 'symmetric', 'clockwise', 'counter-clockwise', 'bidirectional']
		if pattern in patterns:
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
		if cfg_colors is None:
			return

		colors_temp = cfg_colors.split(',')

		try:
			colors_new = []
			for color in colors_temp:
				color_rgb = check_color_hex(str.strip(color))
				if color_rgb is not None:
					colors_new.append(color_rgb)
			if len(colors_new) == len(colors_temp):  # All colors parsed successfully
				self.colors = colors_new
		except ValueError:
			pass

	def apply_preset(self, preset_name):
		if preset_name is None:
			return
		elif self.__preset_applied:
			self.__debug_print("Preset already applied")
			return

		preset_directory = '.\presets\\'

		presets = os.listdir(preset_directory)
		preset_name = preset_name.lower() + '.ini'

		if preset_name in presets:
			self.__preset_applied = True
			self.parse_config(preset_directory + preset_name)
			self.__debug_print("Preset applied:", preset_name)
		else:
			self.__debug_print("No preset applied")

	def get_cfg_key(self, config, config_name, config_section, config_key):
		try:
			var = config[config_section][config_key]
			self.__debug_print(config_name + ":", config_section, config_key, "-", var)
			return var
		except(KeyError):
			self.__debug_print("Error parsing", config_name + ":", config_section, config_key)
			return None

	def __debug_print(self, *args):
		if self.debug_print:
			print(*args)

	def parse_config(self, cfg_name):
		config = configparser.ConfigParser()
		config.read(cfg_name)

		# Presets
		preset_name = self.get_cfg_key(config, cfg_name, 'User Settings', 'preset')
		self.apply_preset(preset_name)

		# Prismatik Settings
		prismatik_host = self.get_cfg_key(config, cfg_name, 'Prismatik', 'host')
		self.host = prismatik_host if prismatik_host is not None else self.host

		prismatik_port = self.get_cfg_key(config, cfg_name, 'Prismatik', 'port')
		if prismatik_port is not None and is_int(prismatik_port):
			self.port = int(prismatik_port)

		prismatik_key = self.get_cfg_key(config, cfg_name, 'Prismatik', 'key')
		self.api_key = prismatik_key if prismatik_key is not None else self.api_key

		# iRacing Settings
		self.__parse_iracing(config, cfg_name)

		# User Settings
		fps = self.get_cfg_key(config, cfg_name, 'User Settings', 'fps')
		if fps is not None and is_int(fps):
			self.framerate = int(fps) if int(fps) <= 60 else 60

		pattern = self.get_cfg_key(config, cfg_name, 'User Settings', 'pattern')
		if pattern is not None and self.check_patterns(pattern):
			self.pattern = pattern

		self.set_colors(self.get_cfg_key(config, cfg_name, 'User Settings', 'colors'))

		off_color = check_color_hex(self.get_cfg_key(config, cfg_name, 'User Settings', 'off_color'))
		self.off_color = off_color if off_color is not None else self.off_color

		try:
			self.single_color = config.getboolean('User Settings', 'single_color')
			self.__debug_print(cfg_name + ":", 'User Settings', 'single_color', "-", self.single_color)
		except (KeyError, configparser.NoSectionError, configparser.NoOptionError):
			self.__debug_print("Error parsing", cfg_name + ":", "User Settings", "single_color")

		try:
			self.bidirectional_color = config.getboolean('User Settings', 'bidirectional_color')
			self.__debug_print(cfg_name + ":", 'User Settings', 'bidirectional_color', "-", self.bidirectional_color)
		except (KeyError, configparser.NoSectionError, configparser.NoOptionError):
			self.__debug_print("Error parsing", cfg_name + ":", "User Settings", "bidirectional_color")

		blink_rate = self.get_cfg_key(config, cfg_name, 'User Settings', 'blink_rate')
		if blink_rate is not None:
			if is_float(blink_rate):
				self.blink_rate = float(blink_rate)
			elif blink_rate.lower() is 'off' or 'none':
				self.blink_rate = 0

		try:
			self.smoothing = config.getboolean('User Settings', 'color_smoothing')
			self.__debug_print(cfg_name + ":", 'User Settings', 'color_smoothing', "-", self.smoothing)
		except (KeyError, configparser.NoSectionError, configparser.NoOptionError):
			self.__debug_print("Error parsing", cfg_name + ":", "User Settings", "color_smoothing")

		data_filtering = self.get_cfg_key(config, cfg_name, 'User Settings', 'data_filtering')
		if data_filtering is not None:
			self.set_filtering(data_filtering)

	def __parse_iracing(self, config, cfg_name):
		custom_range = False
		var_min = self.get_cfg_key(config, cfg_name, 'iRacing', 'var_min')
		var_max = self.get_cfg_key(config, cfg_name, 'iRacing', 'var_max')
		if var_min is not None and var_max is not None \
			and is_float(var_min) and is_float(var_max):
				self.var_min = float(var_min)
				self.var_max = float(var_max)
				custom_range = True

		api_var = self.get_cfg_key(config, cfg_name, 'iRacing', 'var')
		if api_var is not None and \
			((api_var in ir_utils.whitelist) or custom_range):
					self.api_var = api_var

		if self.api_var == 'DriverCarSLBlinkRPM':  # Alias, as listed in the iRacing SDK docs
			self.api_var = 'ShiftLight'
