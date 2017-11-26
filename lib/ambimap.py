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

import lib.lightpack as lightpack

def linear_blend(color1, color2, blendPercent):
	colorOut = []
	for i in range(0, 3):
		m = color2[i] - color1[i]
		newC = (float(m) * blendPercent) + color1[i]
		colorOut.append(int(newC))
	return colorOut

class ambiMap:
	def __init__(self, settings):
		self.settings = settings
		self.ambilight = lightpack.lightpack(settings.host, settings.port, None, settings.apiKey)
		self.initialOn = False

		self.filteredPercent = 0.0
		self.ir_connected = False

	def connect(self):
		self.ambilight.connect()
		if str.rstrip(self.ambilight.getStatus()) == 'on':
			self.initialOn = True

		self.ambilight.lock()
		self.ambilight.turnOn()
		self.ledIndex = self.ambilight.getCountLeds() - 1

	def disconnect(self):
		if self.initialOn == False:
			self.ambilight.turnOff()
		self.initialOn = False
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

	def getColor(self, percent):
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
		self.filteredPercent = ((1 - self.settings.filtering) * self.filteredPercent) \
								+ (self.settings.filtering * percent)
		return self.filteredPercent

	def map(self, percent):
		percent = self.low_pass(percent)
		if percent <= 0.025:
			percent = 0.0

		if self.settings.direction == 'all':
			self.fillAll(self.getColor(percent))
		elif self.settings.direction == 'symmetric':
			self.fillSymmetric(percent, self.getColor(percent))
		elif self.settings.direction == 'clockwise':
			self.fillClockwise(percent, self.getColor(percent))
		elif self.settings.direction == 'counter-clockwise':
			self.fillCClockwise(percent, self.getColor(percent))

	def fillAll(self, color):
		leds = []

		for led in range(0, self.ledIndex + 1):
			leds.append(color)
		self.ambilight.setFrame(leds)

	def fillSymmetric(self, percent, color):
		led_step = percent * (self.ledIndex / 2)
		leds = []

		for led in range(0, self.ledIndex + 1):
			if led <= led_step or led >= self.ledIndex - led_step:
				leds.append(color)
			else:
				leds.append(self.settings.off_color)
		self.ambilight.setFrame(leds)

	def fillClockwise(self, percent, color):
		led_step = (1 - percent) * self.ledIndex
		leds = []

		for led in range(0, self.ledIndex + 1):
			if led >= led_step:
				leds.append(color)
			else:
				leds.append(self.settings.off_color)
		self.ambilight.setFrame(leds)

	def fillCClockwise(self, percent, color):
		led_step = percent * (self.ledIndex)
		leds = []

		for led in range(0, self.ledIndex + 1):
			if led <= led_step:
				leds.append(color)
			else:
				leds.append(self.settings.off_color)
		self.ambilight.setFrame(leds)
