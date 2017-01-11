Installation
============
Theoretically:

.. code-block:: console

   pip install cython numpy scipy gdal
   pip install git+https://github.com/Kortforsyningen/malstroem.git[speedups]


Unfortunately the above doesn't work on all platforms as malstroem uses som third party libraries and has some
optimized code which needs to be compiled for each platform.

Installing on Linux
-------------------
Theory is reality:

.. code-block:: console

   pip install cython numpy scipy gdal
   pip install git+https://github.com/Kortforsyningen/malstroem.git[speedups]


Installing on Windows
---------------------

These instructions are for Python v2.7 64bit. Change accordingly if you prefer another version of Python.

1. `Download <https://www.python.org/downloads/windows/>`_ and install latest Python 2.7 "Windows x86-64 MSI installer"
2. `Download <https://www.microsoft.com/en-us/download/details.aspx?id=44266>`_ and install "Microsoft Visual C++
   Compiler for Python 2.7"
3. Go to `Christoph Gohlke <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_ and download `numpy`, `gdal` and `scipy`
   wheels matching your python. For Python 2.7 64 bit it should be files ending in `cp27‑cp27m‑win_amd64.whl`
4. Open windows command prompt and go to the scripts folder in your Python installation. In a defaut install it should
   be something like

.. code-block:: console

   cd c:\Python27\scripts


5. For each of the 3 wheel files downloaded from Gholke (starting with `numpy`) install it with pip like this:

.. code-block:: console

   pip install c:\downloads\numpy‑1.11.3+mkl‑cp27‑cp27m‑win_amd64.whl


6. Now (finally) install malstroem

.. code-block:: console

   pip install git+https://github.com/Kortforsyningen/malstroem.git[speedups]


7. Still in the scripts folder of your Python (c:\python27\scripts) check that malstroem responds to

.. code-block:: console

   malstroem --help


Installing on Mac OSX
---------------------
The biggest problem on OSX is getting GDAL to work. One known solution is via `homebrew <http://brew.sh/>`_:

1. Make sure homebrew is installed and you know how to use its Python (See for instance `this guide <http://docs.python-guide.org/en/latest/starting/install/osx/>`_)
2. Install GDAL and its Python bindings

.. code-block:: console

   brew install gdal

3. Make sure you use the homebrew Python and install malstroem and its dependencies (If you are using a virtualenv
   create it using `--system-site-packages`)

.. code-block:: console

   pip install cython numpy scipy
   pip install git+https://github.com/Kortforsyningen/malstroem.git[speedups]