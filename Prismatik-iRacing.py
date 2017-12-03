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

import time

import lib.settings as settings
import lib.ambimap as ambimap
import lib.ir_utils as ir_utils

if __name__ == '__main__':
	user_settings = settings.Settings('cfg')
	ambilight = ambimap.AmbiMap(user_settings)
	ir = ir_utils.iRacer()
	low_pass = ambimap.LowPass(user_settings.filtering)

	try:
		while True:
			ir_connection = ir.check_connection()

			if ir_connection == True:
				t = low_pass.filter(ir.api[user_settings.apiVar])
				ambilight.map(t)
				print(user_settings.apiVar + ':', t)
				time.sleep(1 / user_settings.framerate)
			elif ir_connection == "Connected":
				ambilight.connect()
			elif ir_connection == "Disconnected":
				ambilight.disconnect()
			else:
				time.sleep(1)
	except KeyboardInterrupt:
		# press ctrl+c to exit
		pass
