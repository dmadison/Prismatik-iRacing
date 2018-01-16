# iRacing Plugin Presets
Here are some preset configurations for displaying various iRacing data. To use one, set the "preset" variable in the "User Settings" section to one of the available options. Any specified settings in the user config file will overwrite the preset's.

You can make your own custom presets by saving your config file in the 'presets' folder.

## Shift Light (ShiftLight)
```
[iRacing]
var: ShiftLight

[User Settings]
pattern: symmetric
colors: #00FF00, #FFFF00, #FF0000
blink_rate: 2.5
```

This is the default preset that comes with the plugin. It turns the ambilight into a shift light using the car's RPM data and shift points.

## Throttle / Brake / Clutch
```
[iRacing]
var: {see below}

[User Settings]
pattern: clockwise
colors: {see below}
```
You can also match the ambilight to your throttle, brake, or clutch inputs just like the HUD. In iRacing the overlay maps these to green, red, and blue respectively. Note that the plugin only works with one value at a time. The variables and colors for each are listed below.

### Throttle
```
[iRacing]
var: Throttle

[User Settings]
colors: #00FF00
```

### Brake
```
[iRacing]
var: Brake

[User Settings]
colors: #FF0000
```

### Clutch
```
[iRacing]
var: Clutch
var_min: 1.0
var_max: 0.0

[User Settings]
colors: #0000FF
```
Note that the clutch value is inverted as reported by the API. By flipping the min and max value you can make the LEDs reflect the HUD indicator.

## Splits
```
[iRacing]
var: LapDeltaToBestLap
var_min: 2.0
var_max: -2.0

[User Settings]
pattern: bidirectional
colors: #FF0000, #00FF00
single_color: true
bidirectional_color: false
blink_rate: off
```
This preset shows +/- time difference mapped to the LEDs, split along the center just like the sim. You can use any `LapDeltaX` variable for this preset:
* LapDeltaToBestLap
* LapDeltaToOptimalLap
* LapDeltaToSessionBestLap
* LapDeltaToSessionLastlLap
* LapDeltaToSessionOptimalLap

The data inputs are flipped because the typical ambilight setup runs counter-clockwise, and the flipped inputs match the in-game overlay. The default range is +/- 2.0 seconds.

**Note:** This will *not* change based on your splits selection in iRacing (TAB key).

## Oil / Coolant Temperature (Temperature)
```
[iRacing]
var: OilTemp
var_min: {car specific}
var_max: {car specific}

[User Settings]
pattern: clockwise
colors: #0000FF, #FF0000
single_color: true
blink_rate: off
```
Displays the oil temperature or coolant temperature (`WaterTemp`) from blue to red. The range values for what is 'hot' for a given car are not provided by the sim, so you'll need to put in your own values. The temperatures are exposed to the API in Celcius (C).

As these values are user and car-specific, the preset only sets the color pattern. It's up to the user to specify the variable and the range in their config file.

## G-Force Indicator (Gforce)
```
[iRacing]
var: LatAccel
var_min: -24.5
var_max: 24.5

[User Settings]
pattern: bidirectional
single_color: true
bidirectional_color: true
blink_rate: off
```
Turns the ambilight into either a lateral or longitudinal (`LongAccel`) G-force meter. These variables are returned in meters / second, so you need to multiply your desired g-force by 9.8. The default here is +/- 2.5 g.
