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
from lib.utils import linear_blend


class AmbiMap:
	def __init__(self, settings):
		self.settings = settings
		self.ambilight = lightpack.lightpack(settings.host, settings.port, None, settings.api_key)
		self.initial_on = False

		self.__last_blink = time.time()

	def connect(self):
		self.ambilight.connect()
		if str.rstrip(self.ambilight.getStatus()) == 'on':
			self.initial_on = True

		self.ambilight.lock()
		self.ambilight.turnOn()
		self.__num_leds = self.ambilight.getCountLeds()

	def disconnect(self):
		if self.initial_on == False:
			self.ambilight.turnOff()
		self.initial_on = False
		self.ambilight.disconnect()

	def get_color(self, percent):
		if percent <= 0.0:
			return self.settings.off_color

		percent_step = 1.0 / len(self.settings.colors)
		blend_range = percent_step

		if self.settings.smoothing == False:
			for step, color in enumerate(self.settings.colors):
				if percent <= (step + 1) * percent_step:
					return color
			return self.settings.colors[len(self.settings.colors) - 1] # Out of range
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

	def __substitute_color(self, percent, color):
		if color is not None:
			return color

		return self.get_color(percent)

	def map(self, percent):
		color = self.get_color(percent) if self.settings.single_color else None

		if self.settings.direction == 'bidirectional':  # >1 check breaks this pattern
			if self.settings.single_color and self.settings.bidirectional_color:
				color = self.get_color(abs((percent - 0.5) * 2))
			self.fill_bidirectional(percent, color)
			return

		if percent > 1.0 and self.check_blink():
			self.fill_empty()
		elif self.settings.direction == 'all':
			self.fill_all(self.get_color(percent))
		elif self.settings.direction == 'symmetric':
			self.fill_symmetric(percent, color)
		elif self.settings.direction == 'clockwise':
			self.fill_clockwise(percent, color)
		elif self.settings.direction == 'counter-clockwise':
			self.fill_counter_clockwise(percent, color)

	def fill_all(self, color):
		leds = []

		for led in range(0, self.__num_leds):
			leds.append(color)
		self.ambilight.setFrame(leds)

	def fill_symmetric(self, percent, color=None):
		if percent == 0.0:
			self.fill_empty()
			return

		led_half = ((self.__num_leds) / 2)
		led_step = percent * led_half
		leds = []

		for led in range(0, self.__num_leds):
			if led <= led_step:
				leds.append(self.__substitute_color(led / led_step, color))
			elif led >= (self.__num_leds - 1) - led_step:
				led_inverted = (self.__num_leds - 1) - led
				leds.append(self.__substitute_color(led_inverted / led_step, color))
			else:
				leds.append(self.settings.off_color)
		self.ambilight.setFrame(leds)

	def fill_clockwise(self, percent, color=None):
		if percent == 0.0:
			self.fill_empty()
			return

		led_step = (1 - percent) * (self.__num_leds - 1)
		leds = []

		for led in range(0, self.__num_leds):
			if led >= led_step:
				led_inverted = (self.__num_leds - 1) - led
				leds.append(self.__substitute_color(led_inverted / self.__num_leds, color))
			else:
				leds.append(self.settings.off_color)
		self.ambilight.setFrame(leds)

	def fill_counter_clockwise(self, percent, color=None):
		if percent == 0.0:
			self.fill_empty()
			return

		led_step = percent * (self.__num_leds - 1)
		leds = []

		for led in range(0, self.__num_leds):
			if led <= led_step:
				leds.append(self.__substitute_color(led / self.__num_leds, color))
			else:
				leds.append(self.settings.off_color)
		self.ambilight.setFrame(leds)

	def fill_bidirectional(self, percent, color=None):
		led_half = self.__num_leds / 2
		percent_signed = (percent - 0.5) * 2  # Percent rescaled to cover -1.0 / 1.0

		leds = []

		for led in range(0, self.__num_leds):
			if led < led_half:
				led_scaled_side = (led_half - led) / led_half  # LED # scaled for n/2 as positive float
				if percent_signed >= led_scaled_side:
					leds.append(self.__substitute_color(abs(led_scaled_side), color))
				else:
					leds.append(self.settings.off_color)
			else:
				led_scaled_side = -((led + 1 - led_half) / led_half)  # LED # scaled for n/2 as negative float
				if percent_signed <= led_scaled_side:
					leds.append(self.__substitute_color(abs(led_scaled_side), color))
				else:
					leds.append(self.settings.off_color)
		self.ambilight.setFrame(leds)

	def fill_empty(self):
		self.fill_all(self.settings.off_color)

	def check_blink(self):
		if self.settings.blink_rate == 0:
			return False

		time_now = time.time()
		blink_period = (1 / self.settings.blink_rate)

		blink_time = time_now - self.__last_blink

		if blink_time >= blink_period:
			self.__last_blink = time_now

		if blink_time >= blink_period / 2:
			return True  # Lights off
		else:
			return False  # Lights on
