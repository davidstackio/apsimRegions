#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 05 14:57:52 2013

@author: David Stack
"""
import os
import math
from pandas.io import sql as psql
import sqlite3 as lite
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as col

newCmap = col.LinearSegmentedColormap.from_list('PrGr', ['#660066','#FFFFFF','#006600'])
cm.register_cmap(cmap=newCmap) # bias

colors = ['#FFFFFF','#800080','#0000FF','#008000','#FFFF00','#FFA500','#FF0000','#800000']
newCmap = col.ListedColormap(colors, name='discrete')
cm.register_cmap(cmap=newCmap) # discrete colors

colors = ['#FFFFFF','#0000FF','#008000','#FFFF00','#FF0000']
newCmap = col.LinearSegmentedColormap.from_list('rainbow', colors)
cm.register_cmap(cmap=newCmap)

colors.reverse()
newCmap = col.LinearSegmentedColormap.from_list('rainbow_r', colors)
cm.register_cmap(cmap=newCmap)

def _find_min_max(data):
    '''
    Finds min and max value in data.
    
    Parameters
    ----------
    
    Returns
    -------
    Tuple of min and max data: (min, max)
    '''
    return (np.ma.min(data), int(math.ceil(np.ma.max(data)/10.)*10.))
    
#def _setup_axis(data):
#    '''
#    Determines best range and iteration of axis values based on field name.
#    '''
#    # Set default values
#    minVal = None
#    maxVal = None
#    iterVal = None
#    cmap = 'rainbow'
#    extend = 'max'  # can be 'neither', 'both', 'min', or 'max'
#    
#    # for unique scale
#    minVal = np.ma.min(data)
#    maxVal = int(math.ceil(np.ma.max(data)/10.)*10.) # largest number rounded to nearest 10
#    
#    # for uniform scale
#    #minVal = -2500
#    #maxVal = 360
#    
#    # corelation maps
#    #maxVal = -.4
#    #cmap = 'rainbow_r'
#    #extend = 'neither'
#    
#    return maxVal, minVal, iterVal, cmap, extend

def save_map_image(outFilePath, lats, lons, data, units, imageTitle, dpi=300,
                   resolution='i', minVal = None, maxVal = None,
                   iterVal = None, cmap = 'rainbow', extend = 'max'):
    '''
    Saves a map for one year of one field of data.
    
    Resoution -- resolution of boundary database to use. Can be ``c``
 |                       (crude), ``l`` (low), ``i`` (intermediate), ``h``
 |                       (high), ``f`` (full) or None. Default ``c``.
 '''
    if data.size == 0:
        print '*** Warning: No data exists. Figure not saved.'
        return
        
    # create map
    # setup stereographic basemap
    # lat_ts is latitude of true scale
    # lon_0,lat_0 is central point
    # CA: lat_0=37.,lat_st=37.,lon_0=-117.,width=1550000,height=1300000
    plt.figure(figsize=(8.3,6)) # use when colorbar value longer than 5 places so units do not get clipped
    m = Basemap(width=1550000,height=1300000,
        resolution=resolution,projection='lcc',rsphere=(6367000,6367000),\
        lat_ts=37.,lat_0=37.,lon_0=-117.)
    
#    # setup lambert conformal basemap
#    plt.figure(figsize=(6.6,5))
#    m = Basemap(llcrnrlon=-123.3574, llcrnrlat=29.19366, urcrnrlon=-108.4215,
#                urcrnrlat=44.13576, projection='lcc', lat_1=50., lat_2=50.,
#                lon_0=-107., resolution=resolution)
        
    # draw borders
    m.drawcoastlines(linewidth=0.5)
    m.drawcountries()
    m.drawstates()
    
    # Fill land and ocean areas
    waterColor = '#B2E0FC'
    m.fillcontinents(color='0.8', lake_color=waterColor, zorder=0)
    m.drawmapboundary(fill_color=waterColor, zorder=0)
    
    # draw parallels and meridians.
    # labels = [left,right,top,bottom]
    parallels = np.arange(0.,90,5.)
    m.drawparallels(parallels,labels=[1,0,0,0])
    meridians = np.arange(180.,360.,5.)
    m.drawmeridians(meridians,labels=[0,0,0,1])
    
    # grid the data
    x, y = m(lons, lats)
    
    # set min and max value of data if none
    minmax = _find_min_max(data)
    if minVal == None:
        minVal = minmax[0]
    if maxVal == None:
        maxVal = minmax[1]
    
    # plot data
    # get met from filename to determine grid size
    met = os.path.split(outFilePath)[1].split('_')[1]
    
    if '32' in met: # 32 km
        markerSize = 72
    elif '8' in met: # 8 km
        markerSize = 4
    elif '25' in met: # .25 deg
        markerSize = 54   
    else: # ? km
        markerSize = 4
        print '*** Warning: marker size not defined. Using default: {}'.format(markerSize)
    # add points to map
    m.scatter(x, y, c=data, marker='s', s=markerSize, edgecolors='none', cmap=cmap, 
          vmin=minVal, vmax=maxVal)
    # add colorbar
    #cb = m.colorbar(location='bottom',pad="7%")
    cb = m.colorbar(extend=extend)
    
    # set colorbar units
    cb.set_label(units)
    
    # add title
    plt.title(imageTitle, fontsize=18)
    
    # save file
    plt.savefig(outFilePath, dpi=dpi)
    plt.close()
    
def save_timeseries(dfTs, units, outFilePath, imageTitle, dpi=300, ymin=9000, ymax=14000, color='k'):
    '''
    Saves timeseries figure.
    
    Parameters
    ----------
    dfTs : pandas dataframe
        data to save, indexed by year
    units : string
        units of data (for figure axis)
    outFilePath: string
        where to save figure
    imageTitle : string
        title of figure
        
    Returns
    -------
    Saves a timeseries figure.
    '''
    # find years
    years = dfTs.index
    
    # create plot
    dfTs.plot(color=color, legend=False)
    plt.ylabel('({units})'.format(units=units))
    plt.xlabel('')
    plt.grid()
    plt.xlim((years[0],years[-1]))
    plt.xticks(years, (range(years[0],years[-1]+1)))
    plt.ylim((ymin, ymax))
    plt.title(imageTitle)
    plt.savefig(outFilePath, dpi=dpi)

def save_boxplot(filenameOut, imageTitle, data, field, depVar, units, dpi=300,
                 minVal=None, maxVal=None, binSize=None, ymin=0, ymax=25000):
    '''
    Saves a box and whisker plot.
    
    Parameters
    ----------
    
    
    Returns
    -------
    Saves a box and whisker plot.
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    dataBoxplot = []
    if field in ('mint', 'maxt', 'radn'):
        minVal = 0
        maxVal = 45
        binSize = 2
        binList = range(minVal,maxVal+1,binSize)
        for binNum in binList:
            # select depVar data where the data at position field falls within the bin size range
            cond1 = np.where(data[field] >= binNum)[0] # locations where cond1 true
            cond2 = np.where(data[field] < binNum + binSize)[0] # locations where cond2 true
            cond1and2 = np.intersect1d(cond1,cond2)
            dataBoxplot.append(np.array(depVar)[cond1and2])
    elif field in ('soilwat', 'rain'):
        minVal = 0
        maxVal = 1.5
        binSize = 0.1
        binList = range(int(minVal * 10000),int(maxVal * 10000)+1,int(binSize * 10000))
        binList = [x / 10000. for x in binList]
        for binNum in binList:
            # select depVar data where the data at position field falls within the bin size range
            cond1 = np.where(data[field] >= binNum)[0] # locations where cond1 true
            cond2 = np.where(data[field] < binNum + binSize)[0] # locations where cond2 true
            cond1and2 = np.intersect1d(cond1,cond2)
            dataBoxplot.append(np.array(depVar)[cond1and2])
    else:
        print field, 'variable not defined for boxplot. No figure saved.'
        return # do nothing if not predefined
        
    dataBoxplot = np.array(dataBoxplot) # convert from pandas to np array
    plt.boxplot(dataBoxplot, sym='', positions=binList)
    plt.xlabel(field + ' (' + units + ')')
    plt.ylabel(depVar.name + ' (kg/ha)')
    plt.ylim((ymin, ymax))
    plt.title(imageTitle, fontsize=18)
    plt.savefig(filenameOut, dpi=dpi)
    
def save_figures(runId, experiment, crop, dataDir, imageType, variableName=None):
    '''
    Saves all figures.
    
    Parameters
    ----------
    runId : int
        run number
    experiment : string
        experiment name
    crop : string
        name of crop in experiment
    dataDir : string
        directory where data is located
    
    Returns
    -------
    Saves maps and timeseries for the run.
    '''
    
    # set data paths
    dataPath = os.path.join(dataDir, crop, experiment, '{exp}.sqlite'.format(exp=experiment))
    outFileDir = os.path.join(dataDir, crop, experiment, str(runId))
    
    # create folders
    mapsDir = os.path.join(outFileDir, 'maps')
    if not os.path.isdir(mapsDir):
        os.mkdir(mapsDir)
    
    timeseriesDir = os.path.join(outFileDir, 'timeseries')
    if not os.path.isdir(timeseriesDir):
        os.mkdir(timeseriesDir)
    
    # read data as pandas object
    print 'Reading database...'
    con = lite.connect(dataPath)
    
    # get variable of interest
    if variableName != None:
        sql = '''
        SELECT gp.point_id, lat, lon, ao.sow_year, ao.yield, ao.run_id, rp.{variableName}
        FROM apsimOutput ao
        JOIN gridPoints gp ON gp.point_id = ao.point_id
        JOIN runParameters rp ON ao.run_id = rp.run_id
        WHERE ao.run_id = {runId}
        '''.format(runId=runId, variableName=variableName)
        df = psql.read_frame(sql, con)
        variable = df[variableName][0]
    else:
        sql = '''
        SELECT gp.point_id, lat, lon, ao.sow_year, ao.yield, ao.run_id
        FROM apsimOutput ao
        JOIN gridPoints gp ON gp.point_id = ao.point_id
        JOIN runParameters rp ON ao.run_id = rp.run_id
        WHERE ao.run_id = {runId}
        '''.format(runId=runId)
        df = psql.read_frame(sql, con)
        variable = ''
    
    # get met name
    sql = '''
    SELECT met
    FROM runParameters
    WHERE run_id = {runId}
    '''.format(runId=runId)
    met = psql.read_frame(sql, con)['met'][0]
    
    # get years
    years = list(np.unique(df['sow_year']))
    
    # set multi index
    df = df.set_index(['sow_year', 'point_id'])
    #print df.head()
    
    # save maps
    print 'Saving figures...'
    units = 'kg/ha'
    for year in years:
        #print 'Saving map for {year}...'.format(year=year)
        yearlyDf = df.ix[year]
        
        # get lat, lons, and data
        lats = yearlyDf['lat']
        lons = yearlyDf['lon']
        data = yearlyDf['yield']
        
        outFilePath = os.path.join(outFileDir,mapsDir,'{exp}_{met}_{crop}_yield_{variable}_{year}.{imageType}'.format(exp=experiment, met=met, year=year, crop=crop, variable=variable, imageType=imageType))
        imageTitle = '{crop} yield, {met} {year} ({variable})'.format(crop=crop, met=met, year=year, variable=variable)
        save_map_image(outFilePath, lats, lons, data, units, imageTitle, maxVal=22000)
    
    # average by point id for summary figure
    dfSummary = df.groupby(level='point_id').mean()
    lats = dfSummary['lat']
    lons = dfSummary['lon']
    data = dfSummary['yield']
    
    # save summary map
    #print 'Saving summary map...'
    outFilePath = os.path.join(outFileDir,mapsDir,'{exp}_{met}_{crop}_yield_all_{variable}_{y1}-{y2}.{imageType}'.format(exp=experiment, met=met, y1=years[0], y2=years[-1], crop=crop, variable=variable, imageType=imageType))
    imageTitle = '{crop} yield, {met} {start}-{end} ({variable})'.format(crop=crop, met=met, start=years[0], end=years[-1], variable=variable)
    save_map_image(outFilePath, lats, lons, data, units, imageTitle, maxVal=22000)
    
    # average by sow year for timeseries figure
    dfTs = df.groupby(level='sow_year').mean()
    dfTs = dfTs.drop(['lat','lon','run_id'], axis=1)
    dfTs['yield'] = dfTs['yield']
    
    # save timeseries
    #print 'Saving timeseries figure...'
    outFilePath = os.path.join(outFileDir,timeseriesDir,'{exp}_{met}_{crop}_yield_ts_{variable}_{y1}-{y2}.{imageType}'.format(exp=experiment, met=met, y1=years[0], y2=years[-1], crop=crop, variable=variable, imageType=imageType))
    imageTitle = '{crop} yield, {met} {start}-{end} ({variable}), avg(CA, AZ, NV)'.format(crop=crop, met=met, start=years[0], end=years[-1], variable=variable)
    save_timeseries(dfTs, units, outFilePath, imageTitle, ymin=0)

def main():
    startRun = 1
    endRun = 1
    experiment = 'NARRMEANSOW'
    crop = 'maize'
    imageType = 'png'
    variableName = None
    dataDir = 'C:/EaSM_Project/output/experiments'
    
    for runId in xrange(startRun, endRun+1):
        print 'Run :', runId
        save_figures(runId, experiment, crop, dataDir, imageType, variableName)
    
    print '\n***** Done! *****'
    
# Run main() if module is run as a program
if __name__ == '__main__':
    main()