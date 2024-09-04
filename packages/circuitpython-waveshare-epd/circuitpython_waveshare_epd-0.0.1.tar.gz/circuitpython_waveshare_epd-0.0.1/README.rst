Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ssd1680/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/ssd1680/en/latest/
    :alt: Documentation Status


.. image:: https://github.com/FalcoG/CircuitPython_Waveshare_EPD/workflows/Build%20CI/badge.svg
    :target: https://github.com/FalcoG/CircuitPython_Waveshare_EPD/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython `displayio` driver for Waveshare-based ePaper displays

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

* Waveshare Tri-Color ePaper - 2.66inch e-Paper Module (B)

`View the manual from Waveshare <https://www.waveshare.com/wiki/2.66inch_e-Paper_Module_(B)_Manual>`_

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-waveshare-epd/>`_. To install for current user:

.. code-block:: shell

    pip3 install circuitpython-waveshare-epd

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-waveshare-epd

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install circuitpython-waveshare-epd

Usage Example
=============

See `/examples/waveshare_2in66b.py <https://github.com/FalcoG/CircuitPython_Waveshare_EPD/blob/main/examples/waveshare_2in66b.py>`_

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/ssd1680/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/FalcoG/CircuitPython_Waveshare_EPD/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
