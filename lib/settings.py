import configparser
from lib.whitelist import irvar_whitelist as whitelist

def isFloat(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

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

			self.smoothing = config.getboolean('User Settings', 'color_smoothing')
			self.setFiltering(config['User Settings']['data_filtering'])
		except (KeyError, ValueError):
			print("Error parsing cfg")
