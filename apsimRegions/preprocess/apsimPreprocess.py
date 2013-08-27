#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==============================================================================
#     Main program for creating all apsim files and batch script
#==============================================================================
import glob, os
from apsimconfig import new_apsim
import fileio, batch

def _create_apsim_file(runDir, dataPath, config):
    ''' Creates .apsim and associated files.'''
    # remove old .apsim files
    apsimFileList = glob.glob(os.path.join(dataPath,'*.apsim'))
    for apsimFile in apsimFileList:
        os.remove(apsimFile)
    
    # create .apsim file
    new_apsim(dataPath, config)
    
    # create batch file
    batch.create_run_batchfile(runDir, config.apsimModelDir)
    
def preprocess_one(configPath):
    '''
    Preprocesses one APSIM file.
    
    Parameters
    ----------
    configPath : string
        path to where config file is located
        
    Returns
    -------
    Saves a .apsim file based on config.ini settings
    '''
    
    # read configuration file
    if os.path.isfile(configPath):
        config = fileio.Config(configPath)
    else:
        print '*** Warning: {0} does not exist.'.format(configPath)
    
    # set run directory
    runDir = os.path.split(configPath)[0]
    
    # make data directory if it does not already exist
    dataDir = 'data'
    dataPath = os.path.join(runDir, dataDir)
    if not os.path.isdir(dataPath):
        os.mkdir(dataPath)
    
    # Create .apsim file
    _create_apsim_file(runDir, dataPath, config)

def preprocess_many(outputDir, startRun, endRun=None):
    '''
    Sets which runs to preprocess.
    
    Parameters
    ----------
    outputDir : string
        directory where run folders with configuration files are located
    startRun : int
        run number to start on. Should correspond to a folder number.
    endRun : int
        (optional) run number to stop on. Should correspond to a folder number.
        If not provided, will only process run startRun.
        
    Returns
    -------
    Nothing.
    '''
    
    # set runs to process
    if endRun == None:
        endRun = startRun # inclusive
    runs = range(startRun, endRun+1)
    
    for run in runs:
        configPath = os.path.join(outputDir, str(run), 'config.ini')
        preprocess_one(configPath)
        
# Run main() if module is run as a program
if __name__ == '__main__':
    print '---------------------- apsimPreprocess.py ----------------------'
    print 'A preprocessing script for the APSIM crop model.'
    print '----------------------------------------------------------------'
    
    experimentName = 'control'
    outputDir = 'C:/Users/David/Documents/EaSM_Project/output/experiments/maize/{0}'.format(experimentName)
    
    startRun = 1
    endRun = None
    
    print 'Saving .apsim and .bat files...'
    preprocess_many(outputDir, startRun, endRun)
    
    print '\n***** Done! *****'
    
