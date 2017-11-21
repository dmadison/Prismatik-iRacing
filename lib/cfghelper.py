import configparser
import lib.settings as settings
from lib.whitelist import irvar_whitelist as whitelist

def parseConfig(cfgName):
	config = configparser.ConfigParser()
	config.read(cfgName + '.ini')

	try:
		settings.host = config['Lightpack']['host']
		settings.port = int(config['Lightpack']['port'])
		settings.apiKey = config['Lightpack']['key']

		if config['iRacing']['var'] in whitelist:
			settings.apiVar = config['iRacing']['var']

		settings.framerate = int(config['User Settings']['fps'])

		if config['User Settings']['direction'] in settings.directions:
			settings.direction = config['User Settings']['direction']

		settings.smoothing = config.getboolean('User Settings', 'color_smoothing')
	except (KeyError, ValueError):
		print("Error parsing cfg")
