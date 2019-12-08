"""
MicroPython MCP23017 16-bit I/O Expander
https://github.com/mcauser/micropython-mcp23017

MIT License
Copyright (c) 2019 Mike Causer
"""

class Rotary():
	def __init__(self, port, int_pin, clk, dt, sw=None, cb=None, start_val=0, min_val=0, max_val=10):
		self.port = port
		self.clk = clk
		self.dt = dt
		self.sw = sw
		self.cb = cb

		# initial value
		self.value = start_val
		self.min_val = min_val
		self.max_val = max_val

		pins = (1 << clk | 1 << dt)
		if self.sw is not None:
			pins |= 1 << sw

		# input
		self.port.mode |= pins
		# enable pull ups
		self.port.pullup |= pins
		# input inverted
		self.port.input_polarity |= pins
		# enable interrupt
		self.port.interrupt_enable |= pins

		# interrupt pin, set as input
		self.int_pin = int_pin
		self.int_pin.init(mode=int_pin.IN)

		# last 4 states (2-bits each)
		self.state = 0

		self.sw_state = 0

	def _step(self, val):
		self.value = min(self.max_val, max(self.min_val, self.value + val))
		self._callback()

	def _switched(self, val):
		self.sw_state = val
		self._callback()

	def _rotated(self, clk, dt):
		# shuffle left and add current 2-bit state
		self.state = (self.state & 0x3f) << 2 | (clk << 1) | dt
		if self.state == 180:
			self._step(-1)
		elif self.state == 120:
			self._step(1)

	def _callback(self):
		if callable(self.cb):
			self.cb(self.value, self.sw_state)

	def _irq(self, p):
		flagged = self.port.interrupt_flag
		captured = self.port.interrupt_captured
		if self.sw is not None and flagged == (1 << self.sw):
			self._switched((captured >> self.sw) & 1)
		else:
			clk = (captured >> self.clk) & 1
			dt = (captured >> self.dt) & 1
			if (flagged & (1 << self.clk | 1 << self.dt)) > 0:
				self._rotated(clk, dt)

	def start(self):
		self.int_pin.irq(trigger=self.int_pin.IRQ_FALLING, handler=self._irq)
		# clear previous interrupt, if any
		self.port.interrupt_captured

	def stop(self):
		self.int_pin.irq(None)
		# clear previous interrupt, if any
		self.port.interrupt_captured
