Installation
============

On Linux (Ubuntu)
-----------------

Install with pip as:

.. code-block:: shell

    pip install voxpopuli

You have to have espeak and mbrola installed on your system via apt:

.. code-block:: bash

    sudo apt install mbrola espeak


You'll also need some mbrola voices installed, which you can either get on their project page,
and then uppack in `/usr/share/mbrola/<lang><voiceid>/` or more simply by
installing them from the ubuntu repo's. All the voices' packages are of the form
`mbrola-<lang><voiceid>`. You can even more simply install all the voices available
by running:

.. code-block:: bash

    sudo apt install mbrola-*

In case the voices you need aren't all in Ubuntu repository, you can use this convenient little script
that install voices diretcly from `Mbrola's voice repo <https://github.com/numediart/MBROLA-voices>`_

.. code-block:: bash

    # this installs all british english and french voices for instance
    sudo python3 -m voxpopuli.voice_install en fr

.. note::

    To work, this requires that voxpopuli is installed in your "root" python environment.
    You'll have to install it with ``sudo pip3 install voxpopuli``.


On Windows and Mac
------------------

There are no installation instructions for these platforms currently, for
the following reasons:

- On Windows, there used to be an installer distributed by Mbrola's team, but their
  website went down. Installing Mbrola would require that you compile and install it yourself.
  Any documentation on how to do that reliably on a recent version of Windows would be appreciated.
- On MacOS, you'd also have to compile mbrola by yourself. Moreover, espeak and mbrola
  are hardwired to look for voice databases in ``/usr/share/mbrola``, which isn't editable on MacOS anymore.
  ``voxpopuli`` would require some reworking of its internals to be able to work on MacOS.
  (without too much troubles on the user side).
