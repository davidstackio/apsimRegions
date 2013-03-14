# -*- coding: utf-8 -*-
"""
Created on Thu Aug 02 14:02:50 2012

@author: David
"""
import os, csv, glob, sys
from datetime import datetime
import sqlite3 as lite
import tarfile
csv.register_dialect('apsim', delimiter=' ', skipinitialspace=True)

class ScrubError(Exception):
    '''Error for reporting a non-alphanumeric SQL statement.'''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class _Outputfile:
    ''' Represents an outputfile.'''
    def __init__(self, title, apsimVersion, units, outputData):
        self.title = title
        self.apsimVersion = apsimVersion
        self.units = units
        self.outputData = outputData
    
def _read_outputfile(filename):
    ''' Creates an outputfile object by reading a .out file.
    
    Parameters
    ----------
    filename : string
        name of .out file to process
        
    Returns
    -------
    Outputfile object with .out file contents. If .out file is empty, then
    an empty Outfile object is returned (None values and {} for the dicts).
    
    Outputfile 'out' can be accessed as such:
        out.units
            Returns a dictionary with 'fieldName':'fieldUnits' mapping
            
            ex: {'Date': '(mm/dd/yyyy)', 'yield': '(kg/ha)','radn': '(MJ/m^2)',
                'rain': '(mm)', 'mint': '(oC)', 'maxt': '(oC)', 
                'biomass': '(kg/ha)', 'irr_fasw': '(0-1)'}
            (blank) ex: {}
            
        out.title
            Returns the title of the apsim simulation as a string
            
            ex: 'NARR32_maize_00979'
            (blank) ex: None
        
        out.apsimVersion
            Returns the version of APSIM used to run the simulation as a string
            
            ex: '7.4'
            (blank) ex: None
        
        out.outputData
            Returns a dictionary with 'fieldName':[value1, value2...] mapping
            
            ex: {'Date': ['01/01/2000','01/02/2000'], 'yield': ['3500','4000'], 
                 'maxt': ['39.500','45.385'], 'mint': ['23.500','25.385'],
                 'rain': ['44','35'], 'radn': ['23','56'], 
                 'biomass': ['25','45'], 'irr_fasw': ['1.0','0.93']}
            (blank) ex: {}
    '''
    
    # declare variables the script can finish even if the .out file is empty
    outputData = {}
    fieldNames = []
    fieldUnits = []
    title = None
    apsimVersion = None
    
    # read .out file
    with open(filename) as f:
        reader = csv.reader(f, dialect='apsim')
        try:
            for row in reader:
                if reader.line_num >= 5: # main data
                    for field, item in zip(fieldNames, row):
                        outputData[field].append(item)
                elif reader.line_num == 1: # apsim version
                    apsimVersion = ' '.join(row[2:])
                elif reader.line_num == 2: # title of sim
                    title = ' '.join(row[2:])
                elif reader.line_num == 3: # fieldNames
                    fieldNames = row
                    for field in row:
                        outputData[field] = []
                elif reader.line_num == 4: # units
                    fieldUnits = row
        except csv.Error, e:
            print '*** Warning: {0} contains NULL bytes. Consider re-running simulation. {1}\n'.format(filename, e)
    
    # create units dictionary
    units = dict(zip(fieldNames,fieldUnits))
    
    # create Outputfile object
    outputfile = _Outputfile(title, apsimVersion, units, outputData)
    
    return outputfile
    
def _convert_to_sql_date_format(datesOld, unitsOld):
    ''' Converts APSIM format date to SQL format.
    
    Parameters
    ----------
    datesOld : list
        list of dates to convert
    
    unitsOld : string
        old date formatter
        
    Returns
    -------
    Converted dates as a list and date format string used for conversion.
    '''
    
    # get unitsOld ready for date parsing
    unitsOld = unitsOld.strip('(').strip(')')
    unitsOld = unitsOld.replace('yyyy','%Y')
    unitsOld = unitsOld.replace('mm','%m')
    unitsOld = unitsOld.replace('dd','%d')
    
    # convert value to SQL compatable format
    dates = []
    for i, date in enumerate(datesOld):
        date = datetime.strptime(date, unitsOld)
        date = datetime.strftime(date,'%Y-%m-%d')
        dates.append(date)
    
    # set SQL format for units
    units = '(yyyy-mm-dd)'
    
    return dates, units

def _get_field_type(field):
    ''' Finds data type of field.
    
    Parameters
    ----------
    field : string
        field name from apsim output file
    
    Returns
    -------
    The field type.
    '''
    
    realFields = ('yield', 'biomass', 'mint', 'maxt', 'rain', 'radn', 'lai',
                  'irr_fasw')
    textFields = ('Date')
    
    if field in realFields:
        fieldType = 'real'
    elif field in textFields:
        fieldType = 'text'
    else:
        # set default field type to nothing (not to be confused with NULL)
        # this should allow uknown fields to be added without issue
        fieldType = ''
    
    return fieldType
    
def save_output_to_sqlite(filenameList, sqliteFilename='apsimData.sqlite'):
    ''' Save all .out files in current directory to sqlite database file
    with sqliteFilename.
    
    Deletes any previous database.
    
    Parameters
    ----------
    filenameList : list
        list of .out filenames
    sqliteFilename : string
        (optional) output filename of sqlite database
        
    Returns
    -------
    Nothing. Saves sqlite database file.
    '''
    
    # set database table names
    outputTableName = 'apsimOutput'
    fieldTableName = 'outputFields'
    
    # set first outputTableName column header as primary key
    headerList = ['`point_id` integer']
    
    # get field and units information from first .out file that is not empty
    for filename in filenameList:
        outputfile = _read_outputfile(filename)
        if outputfile.outputData != {}:
            for field, unit in outputfile.units.iteritems():
                fieldType = _get_field_type(field)
                headerList.append('`' + field + '` ' + fieldType)
            # set units to save
            unitsRows = outputfile.units.items()
            break
    
    # define outputTableName column headers
    headerLine = ','.join(headerList)
    
    # delete previous database, if any
    if os.path.isfile(sqliteFilename):
        os.remove(sqliteFilename)
        
    # open database
    conn = lite.connect(sqliteFilename)     
    with conn:
        # create table if it doesn't exist
        try:
            if not outputTableName.isalnum():
                raise ScrubError('not all values alpha numeric: '+ outputTableName)
        except ScrubError:
            raise
        sql = "CREATE TABLE IF NOT EXISTS "+outputTableName+" ("+headerLine+")"
        conn.execute(sql)
        
    # read .out files and save to sqldatabase
    for filename in filenameList:
        outputfile = _read_outputfile(filename)
        if outputfile.outputData == {}: # if the .out file is empty
            continue
        
        # get pointId and append to rows
        rows = []
        pointId = int(outputfile.title.split('_')[-1])
        # get legnth of first data item's list
        pointIds = [pointId] * len(outputfile.outputData.values()[0])
        rows.append(pointIds)
        
        for field, unit in outputfile.units.iteritems():
            # convert Date units to SQL compatable format
            if (field == 'date' or field == 'Date') and unit != '(yyyy-mm-dd)':
                values, unit = _convert_to_sql_date_format(outputfile.outputData[field], unit)
            else:
                values = outputfile.outputData[field]
            rows.append(values)
            
        rows = zip(*rows)
    
        # save data to SQLite database
        with conn:
            valuesPlaceholder = ','.join('?' * len(headerList))
            sql = "INSERT INTO " + outputTableName + " VALUES (" + valuesPlaceholder + ")"
            conn.executemany(sql, rows)
    
    # save fields table to SQLite database
    with conn:
        # create table if it doesn't exist
        try:
            if not fieldTableName.isalnum():
                raise ScrubError('not all values alpha numeric: '+ fieldTableName)
        except ScrubError:
            raise
        sql = "CREATE TABLE IF NOT EXISTS "+fieldTableName+" (name text primary key, units text)"
        conn.execute(sql)
        
        # insert fields into table
        sql = "INSERT INTO " + fieldTableName + " VALUES (?,?)"
        conn.executemany(sql, unitsRows)
        
    print sqliteFilename, 'saved to', os.getcwd()
    
def save_output_to_archive(outputFilenameList, filenameOut='apsimData.tar', compression='gz'):
    ''' Save files in outputFilenameList in current directory to a .tar archive
    named filenameOut, overwriting any previously created archive.
    
    Parameters
    ----------
    outputFilenameList : list
        List of files to be archived
    filenameOut : string
        (optional) Filename of tar archive to be saved
    compression : string
        (optional) Type of compression. Either 'None', 'gz' (gzip), or 'bz2' (bzip2).
        
    Returns
    -------
    Nothing, but an archive (*.tar.gz) is saved
    '''
    
    # set compression options
    if compression == None:
        mode = 'w'
    else:
        mode = 'w:{0}'.format(compression)
        filenameOut = filenameOut + '.{0}'.format(compression)
        
    # add file to archive
    numJobs = len(outputFilenameList)
    prevPrint = 0
    with tarfile.open(filenameOut, mode=mode) as tar:
        for counter, outputFilename in enumerate(outputFilenameList):
            percComplete = int(round(float(counter) / numJobs * 100,1))
            if percComplete in xrange(5,101,5) and percComplete != prevPrint:
                print '{0}%'.format(percComplete)
                prevPrint = percComplete
            tar.add(outputFilename)
    print filenameOut, 'saved to', os.getcwd()
    
def main(args):
    ''' Main function for converting Apsim output to SQLite database.
    Also saves .out and .sum files to a tar archive.
    Ex: python utils.py "sqliteFilename.sqlite"
    
    Parameters
    ----------
    sqliteFilename : string
        (optional) database filename
    
    Returns
    -------
    Nothing
    '''
    
    # set variables from command line args
    if len(args) == 2:
        sqliteFilename = args[1]
    else:
        sqliteFilename = 'apsimData.sqlite'
    
    # print info
    print 'Running post processing routine...'
    
    # save .out files as sqlite database
    print 'Compiling .out and .sum files...'
    outFileList = glob.glob('*.out')
    sumFileList = glob.glob('*.sum')
    
    if outFileList == []:
        print 'No files found. Aborting.'
    else:
        print 'Files found:', len(outFileList)
        
        # save .out files to sqlite database
        print 'Saving to SQLite database...'
        save_output_to_sqlite(outFileList, sqliteFilename)
        
        # add .out and .sum files to archive
        print 'Archiving .out and .sum files...'
        outputFilenameList = outFileList + sumFileList
        save_output_to_archive(outputFilenameList)
    
    print '\n***** Done! *****'

# Run main() if module is run as a program
if __name__ == '__main__':
    main(sys.argv)
