import configparser
from lib.whitelist import irvar_whitelist as whitelist

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

		self.parseConfig(self.cfg)

	def checkDirections(self, direction):
		directions = ['all', 'symmetric', 'clockwise', 'counter-clockwise']
		if direction in directions:
			return True
		return False

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
		except (KeyError, ValueError):
			print("Error parsing cfg")



