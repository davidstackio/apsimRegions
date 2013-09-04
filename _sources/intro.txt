.. _intro:

Introduction
************

The apsimRegions is a suite of software tools designed to extend the point-specific Agricultural Production Systems sIMulator (APSIM) crop model to regional spatial scales. It is written in the Python programming language and is currently verified compatible with the Windows version of APSIM 7.4. ApsimRegions is essentially a one-way nested climate-crop modeling framework that links gridded weather data (rain, temperature, radiation, etc.) with the APSIM model. See http://www.apsim.info/Wiki for more information about APSIM. It currently has only been tested with Python 2.7.3. To get started with Python try Python(X,Y) which can be downloaded at http://www.pythonxy.com. The included Spyder IDE is very similar to Matlab.

It is used to create and run .apsim files with many thousands of simulations. Each simulation can represent a unique location or management scenario. The simplest way to use each simulation for different locations would be to create a lookup table with a grid point number and the associated lat and lon. Each simulation would be named from the grid point. Additionally, create a unique .met file for each grid point and reference these in each simulation. It is then possible to loop through all the grid points and create unique simulations (.met file, management rules, soil type, etc.) for each grid point.

