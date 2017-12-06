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

irvar_whitelist = []

# Telemetry variables exposed as floating point percentages - all cars
irvar_global_whitelist = [
	'Brake',
	'BrakeRaw',
	'Clutch',
	'CpuUsageBG',
	'FogLevel',
	'FuelLevelPct',
	'LapDistPct',
	'ShiftIndicatorPct',
	'ShiftPowerPct',
	'SteeringWheelPctDamper',
	'SteeringWheelPctTorque',
	'SteeringWheelPctTorqueSign',
	'SteeringWheelPctTorqueSignStops',
	'Throttle',
	'ThrottleRaw'
]

# Telemetry variables exposed as floating point percentages - selected cars
irvar_restricted_whitelist = [
	'LFwearL',
	'LFwearM',
	'LFwearR',

	'LRwearL',
	'LRwearM',
	'LRwearR',

	'RFwearL',
	'RFwearM',
	'RFwearR',

	'RRwearL',
	'RRwearM',
	'RRwearR',
]

irvar_custom_whitelist = [
	'ShiftLight',
	#'DriverCarSLBlinkRPM',
]

irvar_whitelist.extend(irvar_global_whitelist)
irvar_whitelist.extend(irvar_restricted_whitelist)
irvar_whitelist.extend(irvar_custom_whitelist)
