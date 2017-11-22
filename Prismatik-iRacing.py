
import irsdk
import time

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
	user_settings = settings.settings('cfg')
	ir = irsdk.IRSDK()
	ambilight = ambimap.ambiMap(user_settings)

	try:
		while True:
			check_iracing()
			if ir_connected:
				t = ir[user_settings.apiVar]
				ambilight.map(t)
				print(user_settings.apiVar + ':', t)
				time.sleep(1 / user_settings.framerate)
			else:
				time.sleep(5)
	except KeyboardInterrupt:
		# press ctrl+c to exit
		pass
