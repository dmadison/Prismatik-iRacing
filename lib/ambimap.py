
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

	def getColor(self, percent):
		percent_low = 0.1
		percent_mid = 0.4
		percent_high = 0.95

		if percent == 0.0:
			return [0, 0, 0]

		if self.settings.smoothing == False:
			if percent <= percent_low:
				return self.settings.colors[0]
			elif percent <= percent_mid:
				return self.settings.colors[1]
			else:
				return self.settings.colors[2]
		elif self.settings.smoothing == True:
			if percent <= percent_low:
				return self.settings.colors[0]
			elif percent <= percent_mid:
				return linear_blend(self.settings.colors[0], self.settings.colors[1], (percent - percent_low) / (percent_mid - percent_low))
			elif percent <= percent_high:
				return linear_blend(self.settings.colors[1], self.settings.colors[2], (percent - percent_mid) / (percent_high - percent_mid))
			else:
				return self.settings.colors[2]

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
				leds.append([0, 0, 0])
		self.ambilight.setFrame(leds)

	def fillClockwise(self, percent, color):
		led_step = (1 - percent) * self.ledIndex
		leds = []

		for led in range(0, self.ledIndex + 1):
			if led >= led_step:
				leds.append(color)
			else:
				leds.append([0, 0, 0])
		self.ambilight.setFrame(leds)

	def fillCClockwise(self, percent, color):
		led_step = percent * (self.ledIndex)
		leds = []

		for led in range(0, self.ledIndex + 1):
			if led <= led_step:
				leds.append(color)
			else:
				leds.append([0, 0, 0])
		self.ambilight.setFrame(leds)
