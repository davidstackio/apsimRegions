#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==============================================================================
# main file for creating apsimRegion experiments
#==============================================================================

import os
from apsimRegions.preprocess.configMaker import create_many_config_files
from apsimRegions.preprocess.apsimPreprocess import preprocess_many
from apsimRegions.preprocess.batch import create_run_all_batchfile

def main():
    experimentName = 'test'
    outputDir = 'C:/ExampleProject/output/experiments/maize/{0}'.format(experimentName)
    
    # validArgs are 'resolution','crop','model','crit_fr_asw', 'sowStart', or 'soilName'
    #factorials = {'soilName':['auto','HCGEN0001','HCGEN0003','HCGEN0007','HCGEN0010','HCGEN0011','HCGEN0013','HCGEN0014','HCGEN0015','HCGEN0016','HCGEN0017','HCGEN0025']}
    #factorials = {'sowStart':['auto','01-apr','08-apr','15-apr','22-apr','01-may','08-may','15-may','22-may','01-jun','08-jun','15-jun','22-jun','01-jul']}
    factorials = {'crit_fr_asw':['0.0','0.05','0.15','0.25','0.50','0.75','0.95','1.0']}
    
    otherArgs = {'metFileDir':'C:/ExampleProject/metfiles/working/%(met)s',\
                'gridLutPath':'C:/ExampleProject/lookupTables/exampleLookupTable.csv',\
                'clockStart':'1/1/2001', 'clockEnd':'31/12/2010'}
    
    # create directory if it doesn't exist
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)
    
    # create config files
    print 'Creating configuration files...'
    runs = create_many_config_files(outputDir, factorials, otherArgs)
    
    # create apsim files
    print 'Saving .apsim and .bat files...'
    preprocess_many(outputDir, runs.keys()[0], runs.keys()[-1])
    
    # create run all batchfile
    create_run_all_batchfile(outputDir, runs, experimentName)
    
    # feedback
    print 'All files saved to:\r', outputDir
    print '\nFolder', ': Variable'
    for key in runs.keys():
        print '{0:6} : {1}'.format(key, runs[key])
    
    # save text file of run data
    if not os.path.isfile(os.path.join(outputDir,'readme.txt')):
        mode = 'w'
    else:
        mode = 'a'
        
    with open(os.path.join(outputDir,'readme.txt'),mode=mode) as f:
        f.write('Folder : Variable')
        for key in runs.keys():
            f.write('\n{0:6} : {1}'.format(key, runs[key]))
        f.write('\n')
        
    print '\n***** Done! *****'

# Run main() if module is run as a program
if __name__ == '__main__':
    main()