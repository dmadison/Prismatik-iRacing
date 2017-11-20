
import irsdk
import time

import lib.cfghelper as cfghelper
import lib.settings as settings
import lib.ambimap as ambimap

ir_connected = False


def check_iracing():
	global ir_connected
	if ir_connected and not (ir.is_initialized and ir.is_connected):
		ir_connected = False
		ir.shutdown()
		ambilight.disconnect()
		print('irsdk disconnected')
	elif not ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
		ir_connected = True
		ambilight.connect()
		print('irsdk connected')

if __name__ == '__main__':
	cfghelper.parseConfig('cfg')
	ir = irsdk.IRSDK()
	ambilight = ambimap.ambiMap(settings.host, settings.port, settings.apiKey)
	ambilight.setBlending(settings.smoothing)

	try:
		while True:
			check_iracing()
			if ir_connected:
				t = ir[settings.apiVar]
				ambilight.map(t)
				print(settings.apiVar + ':', t)
				time.sleep(1 / settings.framerate)
			else:
				time.sleep(5)
	except KeyboardInterrupt:
		# press ctrl+c to exit
		pass
