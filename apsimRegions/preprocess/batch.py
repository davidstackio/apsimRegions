#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==============================================================================
#     Module for handling batch file creation
#==============================================================================

import os

def create_run_batchfile(runDir, apsimModelDir):
    '''
    Creates a windows batch file to run apsim using ApsimRun.py.
    
    Parameters
    ----------
    runDir : string
        directory where to save .bat file
    apsimModelDir : string
        directory of apsim model where ApsimRun.py is located
    
    Returns
    -------
    Nothing
    '''
    batchPath = os.path.join(runDir, 'run.bat')
    
    with open(batchPath, 'w') as f:
        f.write('@ECHO OFF\n')
        f.write('TITLE ApsimRun.py\n')
        f.write('CD data\n')
        f.write('"{0}/ApsimRun.py"\n'.format(apsimModelDir))
        #f.write('PAUSE\n')

def create_run_all_batchfile(outputDir, runs, experimentName):
    '''
    Creates a windows batchfile that runs all the other previously
    created batchfiles in each run folder.
    
    Parameters
    ----------
    outputDir : string
        directory where .bat files will be saved
    runs : dictionary
        the keys are run numbers and the values are the varibales
    experimentName : string
        name to save .bat file as
    
    Returns
    -------
    Nothing
    '''
    batchPath = os.path.join(outputDir, 'runAll.bat')
    
    with open(batchPath, 'w') as f:
        f.write('@ECHO OFF\n')
        f.write('ECHO Script for running many ApsimRegions simulations\n')
        f.write('ECHO ------------------------------------------------\n')
        numRuns = len(runs.keys())
        for r, run in enumerate(runs.keys()):
            percComp = (r / float(numRuns)) * 100
            if r == 0:
                f.write('CD {run}\n'.format(run=run))
            else:
                f.write('CD ..\..\{run}\n'.format(run=run))
            f.write('ECHO Running #{run} ({percComp:.1f}%%)...\n'.format(run=run, percComp=percComp))
            f.write('CALL run.bat > run.log\n')
        f.write('ECHO Done!\n')
        f.write('PAUSE\n')