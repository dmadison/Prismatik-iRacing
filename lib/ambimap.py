
import lib.lightpack as lightpack

def linear_blend(color1, color2, blendPercent):
	colorOut = []
	for i in range(0, 3):
		m = color2[i] - color1[i]
		newC = (float(m) * blendPercent) + color1[i]
		colorOut.append(int(newC))
	return colorOut

class ambiMap:
	def __init__(self, _host, _port, _apikey=None):
		self.ambilight = lightpack.lightpack(_host, _port, None, _apikey)
		self.colors = [[0, 255, 0],
					   [255, 255, 0],
					   [255, 0, 0]]
		self.blending = True

	def connect(self):
		self.ambilight.connect()
		self.ambilight.lock()
		self.ambilight.turnOn()
		self.ledIndex = self.ambilight.getCountLeds() - 1

	def disconnect(self):
		self.ambilight.disconnect()

	def setBlending(self, blend):
		if type(blend) is bool:
			self.blending = blend

	def getColor(self, percent):
		percent_low = 0.1
		percent_mid = 0.4
		percent_high = 0.95

		if percent == 0.0:
			return [0, 0, 0]

		if self.blending == False:
			if percent <= percent_low:
				return self.colors[0]
			elif percent <= percent_mid:
				return self.colors[1]
			else:
				return self.colors[2]
		elif self.blending == True:
			if percent <= percent_low:
				return self.colors[0]
			elif percent <= percent_mid:
				return linear_blend(self.colors[0], self.colors[1], (percent - percent_low) / (percent_mid - percent_low))
			elif percent <= percent_high:
				return linear_blend(self.colors[1], self.colors[2], (percent - percent_mid) / (percent_high - percent_mid))
			else:
				return self.colors[2]

	def map(self, percent):
		#self.fillAll(self.getColor(percent))
		self.fillCenter(percent, self.getColor(percent))
		#self.fillClockwise(percent, self.getColor(percent))
		#self.fillCClockwise(percent, self.getColor(percent))

	def fillAll(self, color):
		leds = []

		for led in range(0, self.ledIndex + 1):
			leds.append(color)
		self.ambilight.setFrame(leds)

	def fillCenter(self, percent, color):
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
