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
from lib.utils import LowPass, rescale


def process_frame():
	var = ir.get_data(user_settings.api_var)
	scaled_var = low_pass.filter(rescale(var, user_settings.var_min, user_settings.var_max))
	print(user_settings.api_var + ':', var, '(' + str(scaled_var) + ')')
	ambilight.map(scaled_var)


def framerate_limiter():
	time_start = time.time()
	process_frame()

	frame_time = (1 / user_settings.framerate)
	time_passed = time.time() - time_start
	if time_passed < frame_time:  # Only delay if there is time to waste
		time.sleep(frame_time - time_passed)


if __name__ == '__main__':
	user_settings = settings.Settings('cfg')
	ambilight = ambimap.AmbiMap(user_settings)
	ir = ir_utils.iRacer()
	low_pass = LowPass(user_settings.filtering)

	try:
		while True:
			ir_connection = ir.check_connection()

			if ir_connection == True:
				framerate_limiter()
			elif ir_connection == "Connected":
				ambilight.connect()
			elif ir_connection == "Disconnected":
				ambilight.disconnect()
			else:
				time.sleep(1)
	except KeyboardInterrupt:
		# press ctrl+c to exit
		pass
