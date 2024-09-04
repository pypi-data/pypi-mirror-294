# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 Falco Gerritsjans
#
# SPDX-License-Identifier: MIT
"""
Display driver for Waveshare 2.66inch e-Paper Module (B)

Device:
  - Manual:
    https://www.waveshare.com/wiki/2.66inch_e-Paper_Module_(B)_Manual
  - Product Specification:
    https://files.waveshare.com/upload/e/ec/2.66inch-e-paper-b-specification.pdf

Based on the original display driver for SSD1680-based ePaper displays:
https://github.com/adafruit/Adafruit_CircuitPython_SSD1680
"""

# Display resolution
EPD_WIDTH = 152  # w % 8 must be zero
EPD_HEIGHT = 296  # h % 8 must be zero
EPD_BAUDRATE = 3906250  # 4000_000 # doesn't work for cpy
EPD_CMD_DRIVER_OUTPUT = 0x01  # Driver Output control - display size?
EPD_CMD_GATE_VOLTAGE = 0x03
EPD_CMD_SOURCE_VOLTAGE = 0x04
EPD_CMD_DEEP_SLEEP_MODE = 0x10
EPD_CMD_DATA_ENTRY_MODE = 0x11  # Data Entry mode setting
EPD_CMD_SWRESET = 0x12
EPD_CMD_RAM_SET_X_POS = 0x44
EPD_CMD_RAM_SET_Y_POS = 0x45
EPD_CMD_RAM_SET_X_COUNT = 0x4E
EPD_CMD_RAM_SET_Y_COUNT = 0x4F
EPD_CMD_DISPLAY_UPDATE = 0x20
EPD_CMD_DISPLAY_UPDATE_CTRL_1 = 0x21  # Display Update Control 1
EPD_CMD_DISPLAY_UPDATE_CTRL_2 = 0x22  # Display Update Control 2
EPD_CMD_RAM_WRITE_BW = 0x24  # Write RAM (Black White) / RAM 0x24
EPD_CMD_RAM_WRITE_R = 0x26  # Write RAM (RED) / RAM 0x26)
EPD_CMD_BORDER = 0x3C
EPD_CMD_WRITE_VCOM = 0x2C

CMD_WAIT = 0x80

EPD_VAL_DEEP_SLEEP_MODE_1 = 0x01
EPD_VAL_DEEP_SLEEP_MODE_2 = 0x11

try:
    from epaperdisplay import EPaperDisplay
    from fourwire import FourWire
except ImportError:
    from displayio import EPaperDisplay
    from displayio import FourWire

_CUSTOM_SEQ = [
    # fmt: off
    EPD_CMD_SWRESET, CMD_WAIT, 50,  # wait in ms
    EPD_CMD_DATA_ENTRY_MODE, 0x01, 0x03,  # Ram data entry mode
    EPD_CMD_RAM_SET_X_COUNT, 0x01, 0x01,   # ram x count
    EPD_CMD_RAM_SET_Y_COUNT, 0x02, 0x00, 0x00,  # ram y count
    # EPD_CMD_DRIVER_OUTPUT, 0x03, (EPD_WIDTH - 1) & 0xFF, ((EPD_WIDTH - 1) >> 8) & 0xFF, 0x00,
    EPD_CMD_DISPLAY_UPDATE_CTRL_2, 0x01, 0xf4,  # display update mode
    EPD_CMD_RAM_SET_X_COUNT, 0x00,
    EPD_CMD_RAM_SET_Y_COUNT, 0x00, 0x00,
    # fmt: on
]

_STOP_SEQUENCE = [EPD_CMD_DEEP_SLEEP_MODE, 0x01]  # Deep Sleep


# pylint: disable=too-few-public-methods
class WaveshareEPD(EPaperDisplay):
    r"""Waveshare EPD driver

    :param bus: The data bus the display is on
    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *width* (``int``) --
          Display width
        * *height* (``int``) --
          Display height
        * *rotation* (``int``) --
          Display rotation
    """

    def __init__(self, bus: FourWire, **kwargs) -> None:
        if "colstart" not in kwargs:
            kwargs["colstart"] = 8
        stop_sequence = bytearray(_STOP_SEQUENCE)
        try:
            bus.reset()
        except RuntimeError:
            # No reset pin defined, so no deep sleeping
            stop_sequence = b""

        start_sequence = bytearray(_CUSTOM_SEQ)
        width = kwargs["width"]
        height = kwargs["height"]
        # auto adjust RAM width and height
        if "rotation" in kwargs and kwargs["rotation"] % 180 != 90:
            width, height = height, width

        super().__init__(
            bus,
            start_sequence,
            stop_sequence,
            **kwargs,
            ram_width=height,
            ram_height=width,
            busy_state=True,
            write_black_ram_command=EPD_CMD_RAM_WRITE_BW,
            write_color_ram_command=EPD_CMD_RAM_WRITE_R,
            black_bits_inverted=False,
            set_column_window_command=EPD_CMD_RAM_SET_X_POS,
            set_row_window_command=EPD_CMD_RAM_SET_Y_POS,
            set_current_column_command=EPD_CMD_RAM_SET_X_COUNT,
            set_current_row_command=EPD_CMD_RAM_SET_Y_COUNT,
            refresh_display_command=EPD_CMD_DISPLAY_UPDATE,
            always_toggle_chip_select=False,
            address_little_endian=True
        )
