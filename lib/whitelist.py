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

for item in irvar_global_whitelist:
	irvar_whitelist.append(item)

for item in irvar_restricted_whitelist:
	irvar_whitelist.append(item)
