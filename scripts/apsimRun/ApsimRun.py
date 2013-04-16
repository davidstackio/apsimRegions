# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 22:54:23 2012

@author: David
"""

import subprocess, os, glob, sys
from time import time
from Queue import Queue
import threading
import multiprocessing as mp
from datetime import timedelta, datetime
import utils

# get APSIM install directory (where this module is running from)
apsimPathname = os.path.dirname(sys.argv[0])
apsimPath = os.path.abspath(apsimPathname)
apsimToSimExePath = os.path.join(apsimPath,'ApsimToSim.exe')
if 'win' in sys.platform:
    apsimExePath = os.path.join(apsimPath, 'Apsim.exe')
else: # linux
    apsimExePath = os.path.join(apsimPath, 'Apsim.x')

# set static inputs
counterSim = 0
counterApsim = 0
simFileTotal = 1
apsimFileTotal = 1
old_count = 0
old_average = 0
prevPrint = 0
simRerunAttemps = 0
startTime = time()
numCPU = None

def _update_avg(new_data, old_count, old_average):
    '''Calculates moving average.'''
    new_count = old_count + 1
    new_average = ((old_average * old_count) + new_data) / new_count
    old_count += 1
    old_average = new_average
    return new_average, old_count, old_average

def _cb_apsim(result, lock, timeOld):
    '''Callback function.'''
    global counterApsim
    global apsimFileTotal
    with lock: # keeps counterApsim synchronized
        counterApsim += 1
        percent = int((counterApsim * 100.0)/apsimFileTotal)
        print result, '({0}/{1}) - {2}%'.format(counterApsim,apsimFileTotal,percent)
        
def _run_apsim_to_sim(apsimFilename, lock):
    '''Converts an .apsim file to .sim files.'''
    global apsimToSimExePath
    timeOld = time()
    startupinfo = None
    if 'win' in sys.platform:
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        #si.wShowWindow = 6 # SW_MINIMIZE
        si.wShowWindow = 0 # SW_HIDE - hides cmd windows
        startupinfo=si
    apsimToSimTmpFilename = apsimFilename.replace('.apsim','.tmp')
    with open(apsimToSimTmpFilename, 'w') as tmpFile:
        subprocess.call([apsimToSimExePath, apsimFilename], startupinfo=startupinfo, stdout=tmpFile, stderr=tmpFile)
    
    _cb_apsim(apsimFilename, lock, timeOld)
    
def _worker_apsim(queue, lock):
    '''Process files from the queue.'''
    for args in iter(queue.get, None):
        try:
            _run_apsim_to_sim(args, lock)
        except Exception as e: # catch exceptions to avoid exiting the thread prematurely
            print '{0} failed: {1}'.format(args, e)#, file=sys.stderr
    
def _apsim_exe_run(apsimFilenameList):
    '''Converts .apsim files to .sim files.'''
    global apsimFileTotal
    apsimFileTotal = len(apsimFilenameList)
    print 'Running ApsimToSim for {0} .apsim files...'.format(apsimFileTotal)
    
    # add .sim files to Queue
    q = Queue()
    for apsimFilename in apsimFilenameList:
        q.put_nowait(apsimFilename)
        
    # run .apsim files and start threads to convert
    lock = threading.RLock()
    threads = [threading.Thread(target=_worker_apsim, args=(q,lock)) for _ in range(numCPU)]
    for t in threads:
        t.daemon = False # program quits when threads die
        t.start()
    for _ in threads: q.put_nowait(None) # signal no more files
    for t in threads: t.join() # wait for completion
    
def _cb_sim(result, lock, timeOld):
    '''Callback function.'''
    global counterSim
    global numCPU
    global old_count
    global old_average
    global simFileTotal
    global prevPrint
    with lock: # keeps counterSim synchronized
        counterSim += 1
        percComplete = int(round(float(counterSim) / simFileTotal * 100,1))
        deltaT = time() - timeOld # get runtime
        currentAvg, old_count, old_average = _update_avg(deltaT, old_count, old_average)
        eta = ((simFileTotal - counterSim)*currentAvg/numCPU) + deltaT
        eta = str(timedelta(seconds=round(eta)))
        if percComplete != prevPrint:
            print '{percComplete}% ({counterSim}/{simFileTotal}) - {eta} remaining'.format(counterSim=counterSim,simFileTotal=simFileTotal,percComplete=percComplete,eta=eta)
            prevPrint = percComplete

def _run_sim(simFilename, lock):
    '''Runs a .sim file in APSIM.'''
    global apsimExePath
    global simRerunAttemps
    timeOld = time()
    sumFilename = simFilename.replace('.sim','.sum')
    tmpFilename = simFilename.replace('.sim','.tmp')
    startupinfo = None
    if 'win' in sys.platform:
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        #si.wShowWindow = 6 # SW_MINIMIZE
        si.wShowWindow = 0 # SW_HIDE - hides cmd windows
        startupinfo = si
    with open(tmpFilename, 'w') as tmpFile:
        with open(sumFilename, 'w') as sumFile:
            subprocess.call([apsimExePath, simFilename], stdout=sumFile, stderr=tmpFile, startupinfo=startupinfo)
    with open(tmpFilename, 'r') as tmpFile:
        lineList = tmpFile.readlines()
        #print len(lineList)
        if '100%' in lineList[-1]:
            # delete .sim file after processing
            os.remove(simFilename)
            simRerunAttemps = 0
        elif simRerunAttemps < 5:
            # attempt to re-run sim file at most 5 times
            _run_sim(simFilename, lock)
            simRerunAttemps += 1
        else:
            print 'Unable to process file :', simFilename
            simRerunAttemps = 0
    
    _cb_sim(simFilename, lock, timeOld)
    return sumFilename
    
def _worker_sim(queue, lock):
    '''Process files from the queue.'''
    for args in iter(queue.get, None):
        try:
            _run_sim(args, lock)
        except Exception as e: # catch exceptions to avoid exiting the thread prematurely
            print '{0} failed: {1}'.format(args, e)#, file=sys.stderr
    
def _sim_run(simFilenameList):
    '''Runs apsim in parallel for every .sim file in simFilenameList.'''
    global simFileTotal
    global counterSim
    simFileTotal = len(simFilenameList)
    print 'Running Apsim for {0} .sim files...'.format(simFileTotal)
    
    # Add .sim files to Queue
    q = Queue()
    for simFilename in simFilenameList:
        q.put_nowait(simFilename)
        
    # Run .sim files and start threads
    lock = threading.RLock()
    threads = [threading.Thread(target=_worker_sim, args=(q,lock)) for _ in range(numCPU)]
    for t in threads:
        t.daemon = False # program quits when threads die
        t.start()
    for _ in threads: q.put_nowait(None) # signal no more files
    for t in threads: t.join() # wait for completion

def _apsim_run(apsimFilenameList):
    '''Main section for running all of apsim.'''
    
    # convert each .apsim file to .sim files
    timeOld = time()
    _apsim_exe_run(apsimFilenameList)
    conversionRuntime = str(timedelta(seconds=round(time()-timeOld)))
    
    # find all sim files
    simFilenameList = glob.glob('*.sim')
    
    # run all sim files
    _sim_run(simFilenameList)
    
    return conversionRuntime
    
def _post_run(conversionRuntime):
    ''' Steps to take after main apsim run is complete.'''
    
    # save to database and archive
    print 'Compiling .out and .sum files...'
    outFileList = glob.glob('*.out')
    sumFileList = glob.glob('*.sum')
    if outFileList == [] and sumFileList == []:
        print '*** Warning: No files found. Aborting.'
        databaseRuntime = None
        archiveRuntime = None
    elif outFileList == []:
        print '*** Warning: No .out files found.'
        # add .out and .sum files to archive
        print 'Archiving .sum files...'
        timeOld = time()
        sumFileList = glob.glob('*.sum')
        outputFilenameList = outFileList + sumFileList
        utils.save_output_to_archive(outputFilenameList)
        archiveRuntime = str(timedelta(seconds=round(time()-timeOld)))
        databaseRuntime = None
    else:
        print 'Files found:', len(outFileList) + len(sumFileList)
        
        # save .out files to sqlite database
        print 'Saving SQLite database...'
        timeOld = time()
        utils.save_output_to_sqlite(outFileList)
        databaseRuntime = str(timedelta(seconds=round(time()-timeOld)))
        
        # add .out and .sum files to archive
        print 'Archiving .out and .sum files...'
        timeOld = time()
        sumFileList = glob.glob('*.sum')
        outputFilenameList = outFileList + sumFileList
        utils.save_output_to_archive(outputFilenameList)
        archiveRuntime = str(timedelta(seconds=round(time()-timeOld)))
        
    # clean up (remove .tmp, .out, and .sum files)
    print 'Cleaning up...'
    cleanupFilenameList = glob.glob('*.tmp')
    cleanupFilenameList += glob.glob('*.out')
    cleanupFilenameList += glob.glob('*.sum')
    for filename in cleanupFilenameList:
        os.remove(filename)
    
    hr = '=' * 40
    print '\n' + hr
    print 'Run Summary'
    print hr
    print 'Start time :', str(datetime.fromtimestamp(round(startTime)))
    print 'End time :', str(datetime.fromtimestamp(round(time())))
    if conversionRuntime != None: print 'Conversion runtime :', conversionRuntime
    print 'Average runtime per simulation :', str(timedelta(seconds=round(old_average)))
    if databaseRuntime != None: print 'Save to database runtime:', databaseRuntime
    if archiveRuntime != None: print 'Archive runtime:', archiveRuntime
    print 'Total runtime :', str(timedelta(seconds=round(time()-startTime)))
    print '\n***** Done! *****'
    
def main(args):
    '''Runs all .apsim files in directory.
    
    Example Usage: python .../ApsimRun.py [numCPU]
    
    numCPU : integer
        (optional) Sets to how many processors to use (default=all).'''
    
    print '---------------------- ApsimRun.py ----------------------'
    print 'A batch processing script for the APSIM crop model.'
    print '---------------------------------------------------------'
    
    global numCPU
    global startTime
    
    # set variables from command line args
    if len(args) == 1:
        numCPU = mp.cpu_count()
        print 'CPU count set to use all available processors.'
    elif len(args) == 2:
        if int(args[1]) <= mp.cpu_count():
            numCPU = int(args[1])
        else:
            numCPU = mp.cpu_count()
            print '** Warning: Too many threads. CPU count set to use all available processors.'
    else:
        print 'Error. Please provide valid input.'
        print 'Ex: python ApsimRun.py [numCPU]'
    
    print 'Number of CPU cores to use:', numCPU
    
    # find all apsim files
    apsimFilenameList = glob.glob('*.apsim')
    
    # check to see if there are any sim files already in directory
    # if so, run them. Otherwise, find more.
    simFilenameList = glob.glob('*.sim')
    conversionRuntime = None
    if simFilenameList != []:
        print '** {0} .sim files found!'.format(len(simFilenameList))
        print 'Running .sim files...'
        
        # run all sim files in list
        _sim_run(simFilenameList)
    else:
        print '** No .sim files found!'
        
        # run apsim
        conversionRuntime = _apsim_run(apsimFilenameList)

    _post_run(conversionRuntime)
    
# Run if module is run as a program
if __name__ == '__main__':
    main(sys.argv)
