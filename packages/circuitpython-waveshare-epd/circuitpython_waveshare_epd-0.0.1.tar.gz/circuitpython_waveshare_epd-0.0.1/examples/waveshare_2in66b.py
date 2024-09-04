# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 Falco Gerritsjans
#
# SPDX-License-Identifier: Unlicense
"""Simple test script for 2.66" 296x152 tri-color display.

Supported products:
  * Waveshare 2.66" Tri-Color ePaper Display
    * https://www.waveshare.com/wiki/2.66inch_e-Paper_Module_(B)_Manual
"""

import time
import random
import board
import displayio
import busio
from fourwire import FourWire
from waveshare_epd_driver import WaveshareEPD

displayio.release_displays()

# Display resolution
EPD_WIDTH = 152  # w % 8 must be zero
EPD_HEIGHT = 296  # h % 8 must be zero
EPD_BAUDRATE = 3906250  # 4000_000 in MicroPython
EDP_HIGHLIGHT_COLOR = 0xFF0000  # tertiary color of the EPaperDisplay

# When using the Pico W along with the Waveshare 2in66 B bonnet, this shouldn't have to be changed
RST_PIN = board.GP12
DC_PIN = board.GP8
CS_PIN = board.GP9
BUSY_PIN = board.GP13
SCK_PIN = board.GP10
MOSI_PIN = board.GP11

spi = busio.SPI(SCK_PIN, MOSI=MOSI_PIN)

display_bus = FourWire(
    spi,
    command=DC_PIN,
    reset=RST_PIN,
    chip_select=CS_PIN,
    baudrate=EPD_BAUDRATE,
    polarity=0,
    phase=0,
)

time.sleep(1)

"""
Landscape mode:
- width=EPD_WIDTH
- height=EPD_HEIGHT
- rotation=0 OR 180

Portrait mode:
- width=EPD_HEIGHT
- height=EPD_WIDTH
- rotation=90 OR 270
"""
display = WaveshareEPD(
    display_bus,
    width=EPD_WIDTH,
    # width=EPD_HEIGHT,
    height=EPD_HEIGHT,
    # height=EPD_WIDTH,
    highlight_color=EDP_HIGHLIGHT_COLOR,
    busy_pin=BUSY_PIN,
    rotation=180,
    # rotation=270,
)

g = displayio.Group()

with open("/display-ruler.bmp", "rb") as f:
    pic = displayio.OnDiskBitmap(f)
    t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)

    g.append(t)

    display.root_group = g

    print("Randomized integer to test display update (displayed after 120s):")
    print(random.randint(1, 100))
    display.refresh()

    time.sleep(120)
