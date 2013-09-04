.. _tutorial:

Tutorial
********
Required Software
=================
- `Python 2.7 <http://python.org/>`_ -- `Python(x,y) <https://code.google.com/p/pythonxy/>`_ is the recommended distribution (Windows only) as it has an incredible amount of `included packages <https://code.google.com/p/pythonxy/wiki/StandardPlugins>`_.
- `Apsim 7.4 <http://www.apsim.info/>`_

Dependencies
============
The following Python packages are not included in the Python Standard Library and will need to be installed for ApsimRegions to function properly.
    - `pandas <http://pandas.pydata.org/>`_
    - `lxml <http://lxml.de/>`_
    - `matplotlib <http://matplotlib.org/>`_ (optional - for creating figures)
    - `basemap <http://matplotlib.org/basemap/>`_ (optional - for creating maps)*

\* Does not come with the standard Python(x,y) distribution, and will need to be `installed separately <https://code.google.com/p/pythonxy/wiki/AdditionalPlugins>`_
    
Optional Software
=================
The following software is optional, but may make ApsimRegions easier to use.

- `FileZilla <https://filezilla-project.org/>`_
- `GitHub for Windows <http://windows.github.com/>`_
- `7-Zip <http://www.7-zip.org/>`_ (Windows only)
- `SQLite Studio <http://sqlitestudio.pl/>`_

Installation
============
1.	Synchronize local repository with GitHub repository or download zipped version of ApsimRegions from GitHub.
2.	Run install.bat script. This script may require modifications if Apsim and Python were not installed to their standard directories (typically the C: drive).

Preprocess
==========
1.	Select a name for the experiment. It should be alphanumeric and will be used in all proceeding steps.
2.	Open the preprocess.py script (found in the scripts folder).
3.	Change the experiment name, output directory, factorials, and other arguments as needed for the project.

Run
===
1.	After completing the Preprocessing steps above, navigate to the experiment folder you just created.
2.  Double click the runAll.bat file.
3.  Wait for run to complete.

Post Process
============
1.	Open the masterRunDb.py script. This scrip aggregates the daily data output from Apsim to the yearly scale and saves all run variations to a separate database (located in the root experiment directory).
2.	At the end of the file, change the experiment name to the current experiment, ensure the paths to the files are correct, and change the start and end run parameters accordingly (corresponds to the numbered folders within the experiment directory).
3.  Run the the masterRunDb.py script.
4.  Wait for it to finish.
5.	Create desired figures by reading the database. Examples forthcoming...