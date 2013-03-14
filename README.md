apsimRegions
============

ApsimRegions is a one-way nested climate-crop modeling framework that links gridded weather data (rain, temperature, radiation, etc.) with the point-specific Agricultural Production Systems sIMulator (APSIM) crop model. See http://www.apsim.info/Wiki for more information about APSIM. It currently has only been tested with Python 2.7.3. To get started with Python try Python(X,Y) which can be downloaded at www.pythonxy.com. The included Spyder IDE is very similar to Matlab.

It is used to create and run .apsim files with many thousands of simulations. Each simulation can represent a unique location or management scenario. The simplest way to use each simulation for different locations would be to create a lookup table with a grid point number and the associated lat and lon. Each simulation would be named from the grid point.  Additionally, create a unique .met file for each grid point and reference these in each simulation. It is then possible to loop through all the grid points and create unique simulations (.met file, management rules, soil type, etc.) for each grid point.

- The apsimRegions directory contains code for creating the APSIM files (preprocess). Just move the package to your Python site-packages folder (ie C:\Python27\Lib\site-packages) and import the apsimRegions package by using in Python:

  import apsimRegions as ar

  Call all the funtions by using ar.{function}

- The scrips directory contains code for running APSIM. Copy both apsimRun.py and utils.py to your APSIM installation directory. Run them on Windows from the command line by using the command:

  C:\{data_directory}> "C:/Program Files (x86)/Apsim74-r2286/Model/ApsimRun.py"
  
  from the directory containing .apsim file(s) you wish to run. The associated .out and .sum files will be generated as the script runs, but will be removed after it is completed and the files are archived (*.tar.gz) and saved to a SQLite database. See the run.bat example in the examples folder.