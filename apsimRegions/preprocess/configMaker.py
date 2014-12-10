#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==============================================================================
#     Makes apsimRegions configuration files
#==============================================================================

import ConfigParser, os

def _get_run_num(outputPath):
    '''
    Looks for highest numbered folder in directory. Adds one and
    returns as new run number.
    
    Parameters
    ----------
    outputPath : string
        directory of run locations where output files are saved
    
    Returns
    -------
    The next available run number as an integer
    '''
    
    # set starting run number
    runNum = 0
    
    # get list of all folders and files
    dirContents = os.listdir(outputPath)
    
    # look for higher value runNums, skipping any file/folder that is not
    # castable as an int, thus ignoring non-run numbered folders
    for listing in dirContents:
        try:
            runNumTemp = int(listing)
            if runNumTemp > runNum:
                runNum = runNumTemp
        except ValueError:
            continue
    
    # add 1 for next directory
    runNum += 1
    
    return runNum
    
def _setup_run_dir(outputPath):
    '''
    Creates folders and returns configuration file path.
    
    Parameters
    ----------
    outputPath : string
        location where to save output run folders
        
    Returns
    -------
    Configuration file path.
    '''
    run = _get_run_num(outputPath)
    runDir = os.path.join(outputPath, '{run}'.format(run=run))
    if not os.path.isdir(runDir):
        os.mkdir(runDir)
    configPath = os.path.join(outputPath, runDir, 'config.ini')
    
    return configPath, run
    
def create_config_file(configPath, gridLutPath, metFileDir, \
                        apsimModelDir='C:/Program Files (x86)/Apsim74-r2286/Model',\
                        soilDataPath='C:/Program Files (x86)/Apsim74-r2286/UserInterface/ToolBoxes/hc27_v1_1.soils',\
                        resolution='32', crop='maize', \
                        clockStart='1/1/1991', clockEnd='31/12/2011', \
                        model='NARR', sowStart='auto', soilName='auto',\
                        mass='1000.0', cnr='80.0', cpr='', \
                        standing_fraction='0.0', automatic_irrigation='on', \
                        asw_depth='600', crit_fr_asw='0.95', irrigation_efficiency='1',\
                        irrigation_allocation='off', allocation='0',\
                        density='8', depth='30', cultivar='usa_18leaf', row_spacing='760',\
                        outputVariables='mm/dd/yyyy as date, yield, biomass, lai, rain, mint, maxt, radn, irr_fasw'):
    '''
    Saves an apsimRegions configuration file.
    
    Parameters
    ----------
    configPath : string
        path of where configuration file is to be saved
    gridLutPath : string
        path to grid lookup table
    metFileDir : string
        directory where metfiles are located
    apsimModelDir : string
        (optional) directory where Apsim is installed
    soilDatapath : string
        (optional) path to soil data
    resolution : int or string
        (optional) resolution of simulation
    crop : string
        (optional) crop for simulation
    clockStart : string
        (optional) start date of simulation in dd/mm/yyyy format
    clockEnd : string
        (optional) end date of simulation in dd/mm/yyyy format
    model : string
        (optional) weather information for simulation .met files
    sowStart : string
        (optional) sowing date for simulation
    soilName : string
        (optional) name of soil to use for simulation. If 'auto', it is
        selected from a provided lookup table.
    mass : float or string
        (optional) surface organic matter setting
    cnr : float or string
        (optional) surface organic matter setting
    cpr : float or string
        (optional) surface organic matter setting
    standing_fraction : float or string
        (optional) surface organic matter setting
    automatic_irrigation : string
        (optional) turn on or off automatic irrigation
    asw_depth : float or string
        (optional) depth at which available soil water is calculated
    crit_fr_asw : float or string
        (optional) threshold to irrigate at
    irrigation_efficiency : float
        (optional) irrigation efficiency
    irrigation_allocation : on/off
        (optional) Allocation of irrigation
    allocation : float
        (optional) allocation amount
    density : int
        (optional) density to plant crops in meters
    depth : int
        (optional) depth to plant crops in mm
    cultivar : string
        (optional) type of cultivar to use
    row_spacing : int
        (optional) spacing of rows in mm
    outputVariables : string
        (optional) APSIM variables to output, separated by commas
        
    Returns
    -------
    Saves an apsimRegions configuration file.
    '''
    # set section names
    pre = 'apsimPreprocessor'
    post = 'apsimPostprocessor'
    
    # create config object
    config = ConfigParser.SafeConfigParser()
    
    # -------
    # default
    # -------
    config.set('DEFAULT', 'resolution', str(resolution))
    config.set('DEFAULT', 'gridLutPath', gridLutPath)
    config.set('DEFAULT', 'crop', str(crop))
    config.set('DEFAULT', 'model', str(model))
    config.set('DEFAULT', 'met','%(model)s')
    
    # ------------
    # preprocessor
    # ------------
    config.add_section('apsimPreprocessor')
    
    # data directories
    config.set(pre, 'apsimModelDir', apsimModelDir)
    config.set(pre, 'metFileDir', metFileDir)
    config.set(pre, 'soilDataPath', soilDataPath)
    
    # clock settings
    config.set(pre, 'clock_start', clockStart)
    config.set(pre, 'clock_end', clockEnd)
    
    # soil settings
    config.set(pre, 'soilName', soilName)
    
    # surface organic matter settings
    config.set(pre, 'mass', str(mass))
    config.set(pre, 'cnr', str(cnr))
    config.set(pre, 'cpr', str(cpr))
    config.set(pre, 'standing_fraction', str(standing_fraction))
    
    # irrigation settings
    config.set(pre, 'automatic_irrigation', automatic_irrigation)
    config.set(pre, 'asw_depth', str(asw_depth))
    config.set(pre, 'crit_fr_asw', str(crit_fr_asw))
    config.set(pre, 'irrigation_efficiency', str(irrigation_efficiency))
    config.set(pre, 'irrigation_allocation', irrigation_allocation)
    config.set(pre, 'allocation', str(allocation))
    config.set(pre, 'default_no3_conc', '0.0')
    config.set(pre, 'default_nh4_conc', '0.0')
    config.set(pre, 'default_cl_conc', '0.0')
    
    # management rule: sowing settings
    config.set(pre, 'sow_start', sowStart)
    config.set(pre, 'sow_end', '')
    config.set(pre, 'density', str(density))
    config.set(pre, 'depth', str(depth))
    config.set(pre, 'cultivar', cultivar)
    config.set(pre, 'class', 'plant')
    config.set(pre, 'row_spacing', str(row_spacing))
    
    # management rule: fertilizer settings
    config.set(pre, 'FertAmtCriteria', '50')
    config.set(pre, 'FertDepthCriteria', '50')
    config.set(pre, 'FertDepth', '30')
    config.set(pre, 'FertAmt', '25')
    config.set(pre, 'FertType', 'urea_n')
    
    # harvesting settings
    config.set(pre, 'harvest_date', 'auto')
    
    # output settings
    config.set(pre, 'outputVariables', outputVariables)
    config.set(pre, 'outputEvents', 'end_day')
    
    # tracker settings
    config.set(pre, 'trackerVariables', '')
    
    # -------------
    # postprocessor
    # -------------
    config.add_section('apsimPostprocessor')
    
    # data directories
    config.set(post, 'apsimDbFilename', 'apsimData.sqlite')
    config.set(post, 'nassDbPath', 'C:/Users/David/Documents/EaSM_Project/Data_CropYield/ALL/ALL_county_%(crop)s_yield_1991-2011.sqlite')
    
    # general settings
    config.set(post, 'startDate', '1/1/1991')
    config.set(post, 'endDate', '31/12/2011')
    
    # figure settings
    config.set(post, 'imageType', 'png')
    config.set(post, 'mapRes', 'i')
    config.set(post, 'dpi', '300')
    
    # save the configuration file
    with open(configPath, 'wb') as configfile:
        config.write(configfile)

def create_many_config_files(outputDir, factorials, otherArgs={}):
    '''
    Creates many configuration files by only changing one variable
    at a time.
    
    Parameters
    ----------
    outputDir : string
        directory where run folders will be saved
    factorials : dictionary
        different values for apsim parameters to do factorial simulations
        valid keywords include. Must be a single key with at least one
        value.
        
        Valid keys are:
            - resolution
            - crop
            - model
            - sowStart
            - soilName
            - crit_fr_asw
            - density
            - depth
            - cultivar
            - row_spacing
    otherArgs : dictionary
        (optional) other arguments to change in each factorial run.
        Can have multiple keys, but each key may only have a single value.
    
    Returns
    -------
    The run numbers where the configuration files have been created.
    '''
    
    # set valid arguments for creating config file
    validArgs = ('resolution','crop','model','sowStart','soilName','crit_fr_asw',\
                'density','depth','cultivar','row_spacing')
    
    # go through each key in the **kwargs and save config files
    runs = {}
    for factor in factorials:
        if factor in validArgs:
            variables = factorials[factor]
            for variable in variables:
                # get and setup run path
                configPath, run = _setup_run_dir(outputDir)
                runs[run] = variable
                
                # save configuration file
                if factor == 'resolution':
                    create_config_file(configPath, resolution=variable, **otherArgs)
                elif factor == 'crop':
                    create_config_file(configPath, crop=variable, **otherArgs)
                elif factor == 'model':
                    create_config_file(configPath, model=variable, **otherArgs)
                elif factor == 'sowStart':
                    create_config_file(configPath, sowStart=variable, **otherArgs)
                elif factor == 'soilName':
                    create_config_file(configPath, soilName=variable, **otherArgs)
                elif factor == 'crit_fr_asw':
                    create_config_file(configPath, crit_fr_asw=variable, **otherArgs)
                elif factor == 'density':
                    create_config_file(configPath, density=variable, **otherArgs)
                elif factor == 'depth':
                    create_config_file(configPath, depth=variable, **otherArgs)
                elif factor == 'cultivar':
                    create_config_file(configPath, cultivar=variable, **otherArgs)
                elif factor == 'row_spacing':
                    create_config_file(configPath, row_spacing=variable, **otherArgs)
                
        else:
            print '*** Warning: key "{0}" not a valid argument. Check spelling.'.format(key)
            continue
    
    return runs
    
# Run main() if module is run as a program
if __name__ == '__main__':
    print '---------------------- configMaker.py ----------------------'
    print 'A configuration file maker script for ApsimRegions.'
    print '------------------------------------------------------------'
    
    # input
    outputPath = 'C:/Users/David/Documents/EaSM_Project/output/experiments/maize/NARR32_testing'
    kwargs = {'foo':[1,2,3],'resolution':[8,32],'sowStart':['08-apr','15-apr','22-apr','01-may','08-may','15-may','22-may','01-jun','08-jun']}
    
    # create config files
    runs = create_many_config_files(outputPath, **kwargs)
    
    # feedback
    print 'Folder', ': Variable'
    for key in runs.keys():
        print '{0:6} : {1}'.format(key, runs[key])
    print 'All files saved to:\r', outputPath
    print '\n***** Done! *****'