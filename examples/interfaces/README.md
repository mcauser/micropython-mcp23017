# Interfaces

There are a few interfaces for controlling this device.
They all control the same registers, but provide a different approach.

```python
mcp = mcp23017.MCP23017(i2c, 0x20)
```

## List Interface

Custom getter which gives you one of 16 "VirtualPin" objects, each representing a single pin.

```python
# list interface
mcp[0].input()
mcp[1].input(pullup=1)
mcp[1].input(pullup=1, polarity=1)
mcp[1].input(pullup=1, interrupt_enable=1)
mcp[1].value()
mcp[2].output(value=1)
mcp[3].output(value=0)
```

Each VirtualPin has a reference to it's port and knows which bit it represents.

## Method Interface

The pin method is used to configure a single pin.
Using it's optional arguments, all features of the device are configurable.
Passing in a value performs a write, otherwise it performs a read and returns the value from the GPIO register.

```python
mcp.pin(0, mode=1)
mcp.pin(1, mode=1, pullup=True)
mcp.pin(1)
mcp.pin(2, mode=0, value=1)
mcp.pin(3, mode=0, value=0)

mcp.config(interrupt_polarity=1, sequential_operation=0, interrupt_mirror=0)

mcp.pin(1, mode=1, pullup=1, polarity=0, interrupt_enable=1)
mcp.interrupt_triggered_gpio(port=0)
mcp.interrupt_captured_gpio(port=0)
```

## Property Interface

The device contains two 8-bit ports.
Using this interface you can set both with a 16-bit Integer, or either with 8-bit Integers.
Lower 8-bits are for port a, higher 8-bits are for port b.

Write to both port a and b registers.

```python
mcp.mode = 0xfffe
mcp.mode = 65534
mcp.gpio = 0x0001
mcp.gpio = 1
```

Using this syntax you can toggle pin(s).

```python
mcp.gpio = 0    # set all LOW
mcp.gpio |= 3   # set the first 2 pins HIGH
mcp.gpio &= ~3  # set the first 2 pins LOW
```

Write to the port registers independently.

```python
mcp.porta.mode = 0xfe
mcp.portb.mode = 0xff
mcp.porta.gpio = 0x01
mcp.portb.gpio = 0x00
```

The mcp properties wrap matching properties in each port.

Property                  | Register
------------------------- | --------
mode                      | iodir
input_polarity            | ipol
interrupt_enable          | gpinten
default_value             | defval
interrupt_compare_default | intcon
io_config                 | iocon
pullup                    | gppu
interrupt_flag            | intf
interrupt_captured        | intcap
gpio                      | gpio
output_latch              | olat

The io_config/iocon property is special. Internally, both ports share the same register. Writing to one updates both.
