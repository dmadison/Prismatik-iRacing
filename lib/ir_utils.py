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

import irsdk


class iRacer:
	def __init__(self):
		self.api = irsdk.IRSDK()
		self.api.startup()

	def check_connection(self):
		if self.api.is_initialized and self.api.is_connected:
			return True
		else:
			self.api.startup()
			return False

	def sli_percent(self):
		if self.api['DriverInfo']:
			rpm_min = self.api['DriverInfo']['DriverCarSLFirstRPM']
			rpm_max = self.api['DriverInfo']['DriverCarSLLastRPM']
			rpm_maxB = self.api['DriverInfo']['DriverCarSLBlinkRPM']
			rpm_max_scale = rpm_max - rpm_min

			rpm_current = self.api['RPM']

			if rpm_current >= rpm_maxB:
				return 1.01
			elif rpm_current >= rpm_max:
				return 1.0
			elif rpm_current <= rpm_min:
				return 0.0
			else:
				rpm_current -= rpm_min
				shift_percentage = rpm_current / rpm_max_scale
				return shift_percentage

		return 0.0
