#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==============================================================================
# main file for creating a database of all the experiments' runs
#==============================================================================

import os
import numpy as np
import pandas
from pandas.io import sql as psql
from time import strptime
from math import floor
import sqlite3 as lite
from apsimRegions.preprocess import fileio

def create_tables(masterDbConn, gridLut):
    '''
    Creates each of the tables in the master run database.
    
    Parameters
    ----------
    masterDbConn : sqlite connection object
        master database to connect to
    gridLut : pandas dataframe
        contains the grid information (point_id, lat, lon, county, etc.)
    
    Returns
    -------
    Nothing.
    '''
    with masterDbConn:
        # create runParameters table
        sql = "CREATE TABLE runParameters (run_id INTEGER PRIMARY KEY, met TEXT, crop TEXT, resolution REAL, clock_start TEXT, clock_end TEXT, crit_fr_asw REAL, sow_start TEXT, sow_end TEXT, harvest_date TEXT, soil_name TEXT)"
        masterDbConn.execute(sql)
        
        # create apsimOutput table
        # handeled in update_apsim_output_table()
        
        # create outputFields table
        # handeled in update_output_fields_table()
        
        # create gridPoints table
        psql.write_frame(gridLut, 'gridPoints', masterDbConn)
        
def update_run_parameters_table(masterDbConn, configPath):
    '''
    Updates the runParameters table in the master run database. If a run
    is already there it is updated, otherwise it is added.
    
    Parameters
    ----------
    masterDbConn : sqlite connection object
        master database to connect to
    configPath : string
        path to configuration file which contains all the configuration
        details of the run
    
    Returns
    -------
    If the database is being updated (True) or not (False).
    '''
    # set if the database is being updated or not
    update = False
    
    # read configuration file
    if os.path.isfile(configPath):
        config = fileio.Config(configPath)
    else:
        print '*** Warning: {0} does not exist.'.format(configPath)
        
    # set the variables to save to the runParameters table
    row = config.toDict()
    row['runId'] = int(os.path.split(os.path.split(configPath)[0])[1])
    
    with masterDbConn:
        try:
            sql = "INSERT INTO runParameters VALUES (:runId, :met, :crop, :resolution, :clockStart, :clockEnd, :critFrAsw, :sowStart, :sowEnd, :harvestDate, :soilName)"
            masterDbConn.execute(sql, row)
        except lite.IntegrityError: # for when the row already exists
            sql = "UPDATE runParameters SET run_id=:runId, met=:met, crop=:crop, resolution=:resolution, clock_start=:clockStart, clock_end=:clockEnd, crit_fr_asw=:critFrAsw, sow_start=:sowStart, sow_end=:sowEnd, harvest_date=:harvestDate, soil_name=:soilName WHERE run_id=:runId"
            masterDbConn.execute(sql, row)
            update = True
    
    return update

def _get_yearly_yield(pointDailyData):
    '''
    Determines yield values by year when given daily point data.
    
    Parameters
    ----------
    pointDailyData : pandas TimeSeries
        point daily yield values, indexed by date
    
    Returns
    -------
    Dataframe of yearly yield data (yield and harvest_date).
    '''
    # get unique years from data
    years = np.unique(pointDailyData.index.year)
    
    yearlyYield = {}
    harvestDates = {}
    startDay = pandas.datetime(years[0],1,1)
    yearOverlap = False
    for year in years:
        # check to see if previous year overlaps with this one
        # if it does use the harvest day as start
        if yearOverlap:
            rng = pandas.date_range(startDay, '12/31/{}'.format(year))
        else:
            rng = pandas.date_range('1/1/{}'.format(year), '12/31/{}'.format(year))
        
        # get the max yield for the year and the value on 12/31/{year}
        yearMax = float(pointDailyData.ix[rng].max())
        try:
            yearLastValue = float(pointDailyData.ix[rng[-1]])
        except KeyError as e:
            # special case where previous year's crop is still in ground
            # set current year as NaN and break loop (no more year data)
            print '*** Warning: {e} out of simulation range. Setting year {year} as NaN. Likely due to previous year crop still in ground.'.format(e=e, year=year)
            print '***** Work around: use management rule "end_crop_on_fixed_date_rule" in each APSIM simulation to end the crop at least 2 days before sowing.'
            yearlyYield[year] = np.nan
            harvestDates[year] = np.nan
            raise
            # TODO: BUG (#127)
            # If the chunksize is set to be a static value from the first data
            # point, there is a chance that if there are points where the 
            # simulation abruptly ended, then the chunksizes would be
            # inaccurate from that point forward. Fix this.
            #
            # In cases where the apsim simulation failed to complete, this
            # will cause problems; as when the crop cannot be planted again
            # due to it already existing in the ground.
            #
            # Workaround: delete offending point from the database after
            # the fact.
            break
        
        # if all values are 0 for a given year
        if yearMax == 0:
            yearlyYield[year] = 0
            harvestDates[year] = np.nan
            yearOverlap = False
        # if the last day of the year is 0
        elif yearLastValue == 0:
            yearlyYield[year] = yearMax
            # get timestamp of last possible day that matches yieldMax
            harvestDates[year] = pointDailyData.ix[rng][pointDailyData.ix[rng] == yearMax].tail(1).index[0].strftime('%Y-%m-%d')
            yearOverlap = False
        # if the yield is > 0 on the last day of the year
        elif yearLastValue > 0:
            check = True
            yearOverlap = True
            yearlyYield[year] = yearLastValue
            day = rng[-1]
            while check:
                # get the crop yield for the next day
                day += pandas.DateOffset(1)
                
                # if the date is out of the simulation period 
                # (simulation never completed) then set as NaN
                try:
                    cropYieldNew = float(pointDailyData.ix[day])
                except KeyError as e:
                    # will always happen for the last year of the simulation
                    #print '*** Warning: {e} out of simulation range. Setting year {year} as NaN.'.format(e=e, year=year)
                    yearlyYield[year] = np.nan
                    harvestDates[year] = np.nan
                    cropYieldNew = 0.0
                    check = False
                    
                # check to see if new value is >= preveous day's value
                # if it is, set it as the new value
                # keep checking until the new value is < the old one
                if cropYieldNew >= yearlyYield[year]:
                    yearlyYield[year] = cropYieldNew
                    harvestDates[year] = day.strftime('%Y-%m-%d')
                else:
                    check = False
                    startDay = day
        else:
            print '*** Warning: no case for daily data for year {}'.format(year)
    
    yearlyYield = pandas.Series(yearlyYield)
    harvestDates = pandas.Series(harvestDates)
    
    yearlyYieldData = pandas.DataFrame({'yield':yearlyYield, 
                                   'harvest_date':harvestDates})
                                   
    return yearlyYieldData
    
def _get_avg_data(apsimDbConn, pointDailyData, harvestDates, sowDate):
    '''
    Determines seasonal averages for data.
    
    Parameters
    ----------
    apsimDbConn : sqlite connection object
        connection to database
    dailyData : pandas dataframe
        daily data values, indexed by date
    harvestDates : pandas dataframe
        string date of harvesting, indexed by year
    sowDate : string
        date of sowing (dd-mmm)
        
    Returns
    -------
    Dataframe of yearly average data (rain, mint, maxt, radn, and irr_fasw).
    '''
    # get unique years from data
    years = np.unique(pointDailyData.index.year)
    
    # convert sowDate to correct format
    sowDate = strptime(sowDate,'%d-%b')
    
    # read data from the outputFields table
    with apsimDbConn:
        outputFields = psql.read_frame("SELECT * FROM outputFields;", apsimDbConn)
    outputFields = list(outputFields['name'])
    outputFields.remove('date')
    outputFields.remove('yield')
    
    yearlyAvgData = pandas.DataFrame({})
    for field in outputFields:
        dataAvgs = {}
        for year in years:
            harvestDate = harvestDates[year]
            
            # check if harvestDate is a string
            if type(harvestDate) == type(''):
                rng = pandas.date_range('{0}/{1}/{2}'.format(sowDate.tm_mon, sowDate.tm_mday, year), harvestDate)
                
                # get the avg values and add to dataAvgs dictionary
                pointDailyDataMean = pointDailyData[field].ix[rng].mean()
                dataAvgs[year] = pointDailyDataMean
            else: # if harvestDate is not a string, set as NaN
                dataAvgs[year] = np.nan

        #print dataAvgs
        yearlyAvgData[field] = pandas.Series(dataAvgs)
        #print yearlyAvgData[field].head()
                                   
    return yearlyAvgData
 
def _get_db_info(apsimDbConn, maxChunksize=1500000):
    '''
    Gathers information from the database.
    
    Parameters
    ----------
    apsimDbConn : sqlite connection object
        connection to database
    maxChunksize : int
        (optional) maximum size of the chunks returned fromt the database.
        Use to limit the number of rows returned when experiencing out of
        memory errors.
        
    Returns
    -------
    Point Ids, optimal chunksize based on maxChunksize, and the number of 
    points returned in each query from the database.
    '''
    with apsimDbConn:
        # determine chunksize to read at a time
        pointIds = pandas.io.sql.read_frame("SELECT DISTINCT point_id FROM apsimOutput", apsimDbConn)
    
    # convert to numpy array
    pointIds = np.array(pointIds['point_id'])
    
    with apsimDbConn:
        # assumes that all apsim simulation points have the same number of
        # data points
        # in cases where the apsim simulation failed to complete, this will
        # cause problems.
        pointDataSize = len(pandas.io.sql.read_frame("SELECT point_id FROM apsimOutput WHERE point_id={}".format(pointIds[0]), apsimDbConn))
    
    numPoints = int(floor(maxChunksize / pointDataSize))
    chunksize = pointDataSize * numPoints
    #print 'pointDataSize:', pointDataSize
    
    return pointIds, chunksize, numPoints
    
def _read_apsim_db(apsimDbConn, start, chunksize):
    '''
    Read apsimData.sqlite database.
    
    Parameters
    ----------
    apsimDbConn : sqlite connection object
        connection to database
    start : int
        where to start limiting the data returned
    chunksize : int
        size of chunks to read from the database
        
    Returns
    -------
    A dataframe of daily data.
    '''
    with apsimDbConn:
        # read data from the outputFields table
        outputFields = psql.read_frame("SELECT * FROM outputFields;", apsimDbConn)
        outputFields = list(outputFields['name'])
        outputFields = ', '.join(outputFields)
        
        # read main data
        sql = "SELECT point_id, {outputFields} FROM apsimOutput LIMIT {start}, {chunksize}".format(outputFields=outputFields, start=start, chunksize=chunksize)
        dailyData = pandas.io.sql.read_frame(sql, apsimDbConn)
    
    return dailyData
    
def _apsim_output(apsimDbPath, sowDates):
    '''
    Reads aspim data from the apsim run database.
    
    Parameters
    ----------
    apsimDbPath : string
        path to apsim database
    sowDates : pandas Series
        dates of sowing for each location in the apsim simulation
        (dd-mmm format)
        
    Returns
    -------
    Pandas dataframe of yearly apsim output. Variables that have more than one
    value per year (rain, mint, maxt, radn, etc.) are averaged over the growing
    season.
    '''
    # open database
    apsimDbConn = lite.connect(apsimDbPath)
    
    # get pointIds, numPoints, and chunksize
    print 'Getting database info...'
    pointIds, chunksize, numPoints = _get_db_info(apsimDbConn)
    print 'Number of points per chunk :', numPoints
    
    # read main data
    start = 0
    apsimData = pandas.DataFrame({})
    print 'point num : point_id'
    for p, pointId in enumerate(pointIds):
        print p+1, ':', pointId
        
        # set sow date
        sowDate = sowDates.ix[pointId][0]
        
        # read data in chunks so there will be enough memory
        if p % numPoints == 0:
            print 'Reading from database...'
            dailyData = _read_apsim_db(apsimDbConn, start, chunksize)
            #print dailyData.tail()
            start += chunksize
        
        # set index to date column
        pointDailyData = dailyData[dailyData['point_id'] == pointId]
        pointDailyData = pointDailyData.drop(['point_id'], axis=1)
        pointDailyData = pointDailyData.set_index('date')
        
        # convert to datetime index
        pointDailyData.index = pandas.to_datetime(pointDailyData.index)
    
        # get yearly data
        yearlyYieldData = _get_yearly_yield(pointDailyData['yield'])
        
        # get yearly average data
        harvestDates = yearlyYieldData['harvest_date']
        yearlyAvgData = _get_avg_data(apsimDbConn, pointDailyData, harvestDates, sowDate)
        
        # join yield and avg data, and make pretty
        yearlyData = yearlyYieldData.join(yearlyAvgData)
        yearlyData = yearlyData.reset_index()
        yearlyData = yearlyData.rename(columns={'index':'sow_year'})
        
        # add pointId column to data
        pointIdSeries = pandas.Series([pointId] * len(yearlyData))
        yearlyData['point_id'] = pointIdSeries
        
        apsimData = apsimData.append(yearlyData, ignore_index=True)
        
    return apsimData
    
def update_apsim_output_table(masterDbConn, runPath, update):
    '''
    Updates the apsimOutput table in the master run database. If a run
    is already there it is updated, otherwise it is added.
    
    Parameters
    ----------
    masterDbConn : sqlite connection object
        master database to connect to
    runPath : string
        path to the run folder for the apsimData.sqlite database for a 
        particular run
    update : bool
        if the database needs to be updated or if it is the first commit for a
        particular run
        
    Returns
    -------
    Nothing.
    '''
    # get the runId
    runId = int(os.path.split(runPath)[1])
    
    # don't do anything if the database is being updated
    if update == True:
        print "*** Warning: Run {} data may already exist. Skipping write.".format(runId)
        return
    
    # get sow start from parameters table
    sql = "SELECT sow_start FROM runParameters WHERE run_id = {}".format(runId)
    sowStart = psql.read_frame(sql, masterDbConn).ix[0][0]
    
    # check to see if sow date is auto (determined from lookup table)
    if sowStart == 'auto':
        # read sow start for each location
        sql = "SELECT point_id, sow_start FROM gridPoints"
        sowDates = psql.read_frame(sql, masterDbConn, index_col='point_id')
    else:
        # set sow start the same for each location
        sql = "SELECT point_id FROM gridPoints"
        gridPoints = psql.read_frame(sql, masterDbConn)
        sowDates = pandas.DataFrame([sowStart] * len(gridPoints), index=gridPoints['point_id'])
    
    # get the run database path
    apsimDbPath = os.path.join(runPath, 'data', 'apsimData.sqlite')
    
    # read and convert to yearly formatted data
    apsimData = _apsim_output(apsimDbPath, sowDates)
    
    # add column with runId
    runIdSeries = pandas.Series([runId] * len(apsimData))
    apsimData['run_id'] = runIdSeries
    
    # write runData to master database
    psql.write_frame(apsimData, 'apsimOutput', masterDbConn, if_exists='append')

def update_output_fields_table(masterDbConn, runPath):
    '''
    Updates the outputFields table in the master run database. If a
    field alredy exists it is skipped, otherwise it is added.
    
    Parameters
    ----------
    masterDbConn : sqlite connection object
        master database to connect to
    runPath : string
        path to the run folder for the apsimData.sqlite database for a 
        particular run
        
    Returns
    -------
    A list of fields that were updated in the table.
    '''
    
    # get the run database path
    apsimDbPath = os.path.join(runPath, 'data', 'apsimData.sqlite')
    
    # open run database
    apsimDbConn = lite.connect(apsimDbPath)
    
    with apsimDbConn:
        # read data from the outputFields table
        outputFields = psql.read_frame("SELECT * FROM outputFields;", apsimDbConn)
        
    with masterDbConn:
        # write outputFields to master database
        try:
            psql.write_frame(outputFields, 'outputFields', masterDbConn)
        except ValueError:# as e: # if table already exists then do nothing
            #print '*** Warning: {} Skipping write.'.format(e)
            pass
    
def update_masterDb(masterDbPath, gridLutPath, startRun, endRun):
    '''
    Convenience function for updating everything in the master run
    database.
    
    Parameters
    ---------
    masterDbPath : string
        path to the master run database (../myDocs/runDatabase.sqlite)
    gridLutPath : string
        path to grid lookup table
    startRun : int
        run number to start processing on
    endRun : int
        (optional) run number to stop processing on; inclusive
        
    Returns
    -------
    Nothing.
    '''
    print '---------------------- masterRunDb.py ----------------------'
    print 'A processing script for apsimRegions output from the APSIM'
    print 'crop model. Data is saved to a master run database.'
    print '------------------------------------------------------------'
    
    # set runs to process
    if endRun == None:
        endRun = startRun # inclusive
    runs = range(startRun, endRun+1)
    
    # read grid lookup table
    gridLut = pandas.read_csv(gridLutPath)
    
    # open run database
    # check to see if the file exists. If it doesn't create gridPoints table
    if os.path.isfile(masterDbPath):
        masterDbConn = lite.connect(masterDbPath)
    else:
        # first time opening it
        masterDbConn = lite.connect(masterDbPath)
        
        # create tables
        create_tables(masterDbConn, gridLut)
        
    # update database with data from each run
    numRuns = len(runs)
    with masterDbConn:
        for r, run in enumerate(runs):
            # print progress
            print 'Saving run: {0} ({1}/{2})...'.format(run, r+1, numRuns)
            
            # get paths
            runPath = os.path.join(os.path.split(masterDbPath)[0], str(run))
            configPath = os.path.join(runPath, 'config.ini')
            
            # update runParameters table
            update = update_run_parameters_table(masterDbConn, configPath)
            
            # update apsimOutput table
            update_apsim_output_table(masterDbConn, runPath, update)
            
            # update outputFields table
            update_output_fields_table(masterDbConn, runPath)
                
    print '\n***** Done! *****'

# Run if module is run as a program
if __name__ == '__main__':
    experiment = 'example'
    masterDbPath = 'C:/ExampleProject/output/{exp}/{exp}.sqlite'.format(exp=experiment)
    gridLutPath = 'C:/ExampleProject/lookupTables/exampleLookupTable.csv'
    startRun = 1
    endRun = 1
    update_masterDb(masterDbPath, gridLutPath, startRun, endRun)
