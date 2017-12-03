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

def linear_blend(color1, color2, blend_percent):
	color_out = []
	for i in range(0, 3):
		m = color2[i] - color1[i]
		newC = (float(m) * blend_percent) + color1[i]
		color_out.append(int(newC))
	return color_out


def is_float(x):
	try:
		float(x)
		return True
	except ValueError:
		return False


def check_color_hex(color):
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


class LowPass:
	def __init__(self, filter_weight, zero_threshold=0.025):
		self.__weight = filter_weight
		self.__zero_threshold = zero_threshold

		self.__filtered = 0.0

	def filter(self, percent):
		self.__filtered = ((1 - self.__weight) * self.__filtered) \
								  + (self.__weight * percent)

		if self.__filtered <= self.__zero_threshold:
			return 0.0
		else:
			return self.__filtered
