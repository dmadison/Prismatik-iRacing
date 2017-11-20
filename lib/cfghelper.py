import configparser
import lib.settings as settings

def parseConfig(cfgName):
	config = configparser.ConfigParser()
	config.read(cfgName + '.ini')

	try:
		settings.host = config['Lightpack']['host']
		settings.port = int(config['Lightpack']['port'])
		settings.apiKey = config['Lightpack']['key']

		settings.apiVar = config['iRacing']['var']

		settings.framerate = int(config['User Settings']['fps'])
		settings.smoothing = config.getboolean('User Settings', 'color_smoothing')
	except (KeyError, ValueError):
		print("Error parsing cfg")
