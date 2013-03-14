apsimRegions
============

ApsimRegions is a one-way nested climate-crop modeling framework that links gridded weather data (rain, temperature, radiation, etc.) with the point-specific Agricultural Production Systems sIMulator (APSIM) crop model.

- The apsimRegions directory contains code for creating the APSIM files (preprocess). Just import the apsimRegions package by using:
  import apsimRegions as ar

  Call all the funtions by using ar.{function}

- The scrips directory contains code for running APSIM. Copy both apsimRun.py and utils.py to your APSIM installation directory. Run them on Windows by using the command:
  C:\{data_directory}> "C:/Program Files (x86)/Apsim74-r2286/Model/ApsimRun.py"
  
  from the directory containing .apsim files. The associated .out and .sum files will be generated as the script runs,     but will be removed after it is completed and they are archived (*.tar.gz) and saved to a SQLite database.
