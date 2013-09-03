.. _tutorial:

Tutorial
********
Required Software
=================
- `Apsim 7.4 <http://www.apsim.info/>`_
- `Python 2.7 <http://python.org/>`_ -- `Python(x,y) <https://code.google.com/p/pythonxy/>`_ is the recommended distribution (Windows only)
- **Dependencies** : The following Python packages are not included in the Python Standard Library.
    - numpy
    - matplotlib
    - basemap*
    - pandas

\* Will need to be `installed separately <https://code.google.com/p/pythonxy/wiki/AdditionalPlugins>`_ from Python(x,y)
    
Optional Software
=================
The following software is optional, but may make ApsimRegions easier to use.

- `FileZilla <https://filezilla-project.org/>`_
- `GitHub for Windows <http://windows.github.com/>`_
- `7-Zip <http://www.7-zip.org/>`_ (Windows only)
- `SQLite Studio <http://sqlitestudio.pl/>`_

Installation
============
1.	Synchronize local repository with Github repository or download zipped version of ApsimRegions from Github.
2.	Run install.bat script. This script may require modifications if Apsim and Python were not installed to their standard directories (typically the C: drive).

Preprocess
==========
1.	Select a name for the experiment. It should be alphanumeric and will be used in all proceeding steps.
2.	Open the main.py script.
3.	Change the experiment name, output directory, factorials, and other arguments as needed for the project.

Run
===
1.	In the main experiment folder, double click the runAll.bat file.

Post Process
============
1.	Open the masterRunDb.py script. This scrip aggregates the daily data to the yearly scale and saves all run variations to a separate database.
2.	At the end of the file, change the experiment name to the current experiment, ensure the paths to the files are correct, and change the start and end run parameters accordingly.
3.	Copy the figures.py script template and rename to current experiment name.
4.	Change the crop, start run, end run, and experiment name (near the bottom of the file) accordingly.
5.	Edit the figures.py file, changing settings to produce the figures desired.
    a.	_setup_axis(): map parameters
    b.	Timeseries(): timesereies parameters