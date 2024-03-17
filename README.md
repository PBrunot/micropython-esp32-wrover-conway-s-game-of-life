# micropython-esp32-wrover-conway-s-game-of-life
_Forked from micropython-esp32-ssd1306-conway-s-game-of-life_

Conway's game of life in MicroPython, runs on ESP32 Wrover kit V4 : see [Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/hw-reference/esp32/get-started-wrover-kit.html)

## Game of life

* See [Wikipedia article](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

## Requirements

* Display library: uses ili93xx driver from nano-gui library (see [Github](https://github.com/peterhinch/micropython-nano-gui))
* Install pre-requisites with board connected to WiFi:

```python
import mip
mip.install("github:peterhinch/micropython-nano-gui")
mip.install("github:peterhinch/micropython-nano-gui/drivers/ili93xx")
```

* Copy <code>life.py</code> and <code>color_setup.py</code> on ESP32 board

* Consider increasing clock speed in <code>boot.py</code>

```python
import machine
machine.freq(240_000_000)
```

* Test display is working fine (<code>color_setup.py</code> config)

```python
import gui.demos.aclock
```

* Run Game of Life

```python
import life
```

## Implementation notes

* Updated to Micropython 1.22 (umodules deprecated)
* Rewritten boundary conditions from original implementation: extending the array by 1 cell in all directions, the special cases can be eliminated
* Added pixel size configuration for 320x240 display size
* Various speed improvements with framebuf primitives and viper usage
* Added display of generation number and active cells count on top line
* Tested with ESP32 WroverKit 4.1 with the following image

```shell
 version -- 3.4.0; MicroPython v1.22.2 on 2024-02-22
 implementation -- (name='micropython', version=(1, 22, 2, ''), _machine='Generic ESP32 module with SPIRAM with ESP32', _mpy=10758)
```