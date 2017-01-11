malstroem
=========



Quick start
-------------------------

To use malstroem, do the following, preferably in
a virtual environment. Clone the repo.

.. code-block:: console

    git clone https://github.com/septima/malstroem
    cd malstroem


Development
---------------------------
Then install in locally editable (``-e``) mode and run the tests.

.. code-block:: console

    pip install -e .[test]
    py.test

If you want to run the speedups they need to be compiled at installation time.

.. code-block:: console

    pip install -e .[test,speedups]
    py.test

Another option is using ``tox`` to run the above tests in both Python2 and Python3 in one go.

Install tox.

.. code-block:: console

    pip install tox
    
Run tox.

.. code-block:: console

    tox

Windows notes
----------------------------
Some dependencies (``numpy``, ``gdal`` & ``scipy``) for ``malstroem`` are available
via OSGeo4W. Unfortunately ``pip`` is not always aware of packages installed with
OSGeo4W. ``scipy`` tends to a trouble maker in that regard. A work-around is to
remove the OSGeo4W-``scipy`` and install from a different source. Christop Gohlke's
`Unoffical Windows Binaries <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_ is a good place to start.



Raw Windows install
-------

Install python 2.7


GDAL fra Gholke (husk pyversion)
numpy+mkl fra Gholke
scipy fra gholke



[Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266)


pip install gdalxxxxx.whl


Development
-----------
sphinx-apidoc --full -a -H malstroem -A "Asger Skovbo Petersen, Septima" -v 0.0.1 -o docs malstroem
cd docs
make html

Documentation
-------------

Written in restructuredText and compiled using sphinx.

Needs ReadTheDocs theme:

pip install sphinx_rtd_theme

Make html documentation:

cd docs
make html

Make pdf documentation

cd docs
make latexpdf

The binary pdflatex needs to be available in path.

On OSX:
brew cask install mactex

then

export PATH=/Library/TeX/texbin:$PATH
cd docs
make latexpdf