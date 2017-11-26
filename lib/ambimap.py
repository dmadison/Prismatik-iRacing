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

import time
import lib.lightpack as lightpack


def linear_blend(color1, color2, blend_percent):
	color_out = []
	for i in range(0, 3):
		m = color2[i] - color1[i]
		newC = (float(m) * blend_percent) + color1[i]
		color_out.append(int(newC))
	return color_out


class AmbiMap:
	def __init__(self, settings):
		self.settings = settings
		self.ambilight = lightpack.lightpack(settings.host, settings.port, None, settings.api_key)
		self.initial_on = False

		self.filtered_percent = 0.0
		self.last_blink = time.time()
		self.ir_connected = False

	def connect(self):
		self.ambilight.connect()
		if str.rstrip(self.ambilight.getStatus()) == 'on':
			self.initial_on = True

		self.ambilight.lock()
		self.ambilight.turnOn()
		self.led_index = self.ambilight.getCountLeds() - 1

	def disconnect(self):
		if self.initial_on == False:
			self.ambilight.turnOff()
		self.initial_on = False
		self.ambilight.disconnect()

	def check_iracing(self):
		if self.ir_connected and not self.settings.ir.check_connection():
			self.ir_connected = False
			self.settings.ir.shutdown()
			self.disconnect()
			print('irsdk disconnected')
		elif not self.ir_connected and self.settings.ir.check_connection():
			self.ir_connected = True
			self.connect()
			print('irsdk connected')

	def get_color(self, percent):
		if percent == 0.0:
			return self.settings.off_color

		percent_step = 1.0 / len(self.settings.colors)
		blend_range = percent_step

		if self.settings.smoothing == False:
			for step, color in enumerate(self.settings.colors):
				if percent <= (step + 1) * percent_step:
					return color
		elif self.settings.smoothing == True:
			for step in range(len(self.settings.colors) - 1):
				current_step = (step + 1) * percent_step
				blend_min = current_step - (blend_range / 2)
				blend_max = current_step + (blend_range / 2)
				if percent >= blend_min and percent <= blend_max:
					blend_percent = (percent - blend_min) / (blend_max - blend_min)
					return linear_blend(self.settings.colors[step], self.settings.colors[step + 1], blend_percent)
				elif percent <= current_step:
					return self.settings.colors[step]
			return self.settings.colors[len(self.settings.colors) - 1]

	def low_pass(self, percent):
		self.filtered_percent = ((1 - self.settings.filtering) * self.filtered_percent) \
								+ (self.settings.filtering * percent)
		return self.filtered_percent

	def map(self, percent):
		percent = self.low_pass(percent)
		if percent <= 0.025:
			percent = 0.0

		nextframe = []
		if percent > 1.0 and self.check_blink():
			nextframe = self.fill_empty()
		elif self.settings.direction == 'all':
			nextframe = self.fill_all(self.get_color(percent))
		elif self.settings.direction == 'symmetric':
			nextframe = self.fill_symmetric(percent, self.get_color(percent))
		elif self.settings.direction == 'clockwise':
			nextframe = self.fill_clockwise(percent, self.get_color(percent))
		elif self.settings.direction == 'counter-clockwise':
			nextframe = self.fill_cclockwise(percent, self.get_color(percent))

		self.ambilight.setFrame(nextframe)

	def fill_all(self, color):
		leds = []

		for led in range(0, self.led_index + 1):
			leds.append(color)
		return leds

	def fill_symmetric(self, percent, color):
		led_step = percent * (self.led_index / 2)
		leds = []

		for led in range(0, self.led_index + 1):
			if led <= led_step or led >= self.led_index - led_step:
				leds.append(color)
			else:
				leds.append(self.settings.off_color)
		return leds

	def fill_clockwise(self, percent, color):
		led_step = (1 - percent) * self.led_index
		leds = []

		for led in range(0, self.led_index + 1):
			if led >= led_step:
				leds.append(color)
			else:
				leds.append(self.settings.off_color)
		return leds

	def fill_cclockwise(self, percent, color):
		led_step = percent * (self.led_index)
		leds = []

		for led in range(0, self.led_index + 1):
			if led <= led_step:
				leds.append(color)
			else:
				leds.append(self.settings.off_color)
		return leds

	def fill_empty(self):
		return self.fill_all(self.settings.off_color)

	def check_blink(self):
		time_now = time.time()
		blink_period = 0.400

		blink_time = time_now - self.last_blink

		if blink_time >= blink_period:
			self.last_blink = time_now

		if blink_time >= blink_period / 2:
			return True  # Lights off
		else:
			return False  # Lights on
