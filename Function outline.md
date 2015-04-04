Function outline

Power / Boot
-Key switch for PSU on
-Illuminated rocker switch for RPI on
--illuminated push button:
---short press 'connect to printer'
---long press = shutdown pi
-Missile switch for printer on

Display: How many lines effectively?
-current status
-hot end temp
-bed temp
-time remaining, layer progress
-Current file printing?

Printer controls
-timelapse on / off
-xyze jog
-xyz home
-select axis, select move size



Program structure:

once per second, get status / data

if printer status = printing, disable controls, else poll selectors and update display

callbacks for button presses.