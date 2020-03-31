# Rotary Encoder Example

An example using a rotary encoder as a kind of volume control.

MCP23017 is configured with 3 input pins setup to fire an interrupt on change.

The Rotary class takes care of the calculations and you simply provide it a callback
to fire when the value changes or the switch is pressed.

## Connections

Encoder | MCP23017
------- | --------
CLK     | A3
DT      | A4
SW      | A5
VIN     | 3V3
GND     | GND

MCP23017 | TinyPICO
-------- | ------------
SCL      | GPIO22 (SCL)
SDA      | GPIO21 (SDA)
INTA     | GPIO4
VIN      | 3V3
GND      | GND

## Example

```python
from machine import Pin, I2C
import mcp23017
import rotary
i2c = I2C(scl=Pin(22), sda=Pin(21))
mcp = mcp23017.MCP23017(i2c)

# interrupt pin
p4 = Pin(4, mode=Pin.IN)

# encoder pins
sw_pin = 5
clk_pin = 4
dt_pin = 3

# callback with unicode art
def cb(val, sw):
	volume = '\u2590' * val + '\xb7' * (10 - val)
	if sw:
		btn = '\u2581\u2583\u2581'
	else:
		btn = '\u2581\u2587\u2581'
	print(volume + ' ' + btn)

# simpler callback with just values
def cb(val, sw):
	print('value: {}, switch: {}'.format(val, sw))

# init
r = rotary.Rotary(mcp.porta, p4, clk_pin, dt_pin, sw_pin, cb)

# add irq
r.start()

# remove irq
r.stop()
```
