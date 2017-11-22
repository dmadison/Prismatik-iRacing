import configparser
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
			self.host = config['Lightpack']['host']
			self.port = int(config['Lightpack']['port'])
			self.apiKey = config['Lightpack']['key']

			if config['iRacing']['var'] in whitelist:
				self.apiVar = config['iRacing']['var']

			self.framerate = int(config['User Settings']['fps'])

			if self.checkDirections(config['User Settings']['direction']):
				self.direction = config['User Settings']['direction']

			self.setColors(config['User Settings']['colors'])
			self.smoothing = config.getboolean('User Settings', 'color_smoothing')
			self.setFiltering(config['User Settings']['data_filtering'])
		except (KeyError, ValueError):
			print("Error parsing cfg")
