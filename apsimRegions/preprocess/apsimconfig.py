#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==============================================================================
#     Configuration for setting APSIM run parameters and structure
#==============================================================================

import os, posixpath
from pandas import read_csv, DateOffset
from datetime import datetime
import apsim, soils
import managementRules as manager
    
def setup_project(projectName):
    '''Sets up project options for all simulations.'''
    version = '29'
    doc = apsim.new_document(version, projectName)
    return doc

def setup_met(met, metFileDir, gridpoint):
    '''Returns a met filename for inclusion in .apsim file.

    example item: 'WRF_00979.met'.'''
    met_path = posixpath.join(metFileDir,met+'_'+str(gridpoint).zfill(5)+'.met')
    return met_path

def setup_soils(element, soilDataPath):
    '''Sets up soils for all simulations.'''
    soilsDir = os.path.dirname(soilDataPath)
    soilDataFilename = os.path.basename(soilDataPath)
    origDir = os.getcwd()
    os.chdir(soilsDir)
    soils.add_soils(element, soilDataFilename)
    os.chdir(origDir)
    
def setup_shared_management_options(folder, crop, config, shortcut=None):
    '''Sets up management options for all simulations.'''
    harvestDate = config.harvestDate
    
    # setup management rules based on crop type
    # some crops require certain rules to work
    if crop == 'maize':
        # fertilise rule
        fertilizeRule = manager.fertOnSoilNCriteria_rule(folder,
                                                 FertAmtCriteria=config.fertAmtCriteria,\
                                                 FertDepthCriteria=config.fertDepthCriteria,\
                                                 FertDepth=config.fertDepth,\
                                                 FertAmt=config.fertAmt,\
                                                 FertType=config.fertType)
        # harvesting rule
        if harvestDate == 'auto':
            harvestRule = manager.harvesting_rule(folder, crop)
        else:
            harvestRule = manager.harvest_on_fixed_date_rule(folder, crop, harvestDate=harvestDate)
        
        rulesList = [(fertilizeRule.get('name'),'manager2'),\
                     (harvestRule.get('name'),'manager')]
    elif crop == 'cotton':
        # irrigation rule
        irrigateRule = manager.irrigate_on_sw_deficit_rule(folder)
        
        # fertilise rule
        fertilizeRule = manager.fertOnSoilNCriteria_rule(folder)
        
        # harvesting rule
        if harvestDate == 'auto':
            harvestRule = manager.harvesting_rule(folder, crop)
        else:
            harvestRule = manager.harvest_on_fixed_date_rule(folder, crop, harvestDate=harvestDate)
        
        rulesList = [(irrigateRule.get('name'),'manager'),\
                     (fertilizeRule.get('name'),'manager2'),\
                     (harvestRule.get('name'),'manager')]            
    return rulesList
    
def setup_management_options(folder, crop, config, gridpoint, gridLut, shortcut, rulesList, soil):
    '''
    Setup management rules based on grid cell.
    
    REMEMBER: order matters!
    '''
    # reset water, nitrogen, and surfaceOM rule
    #manager.reset_on_sowing(folder, crop, soilmodule=soil.get('name'))
    
    # set dates from config file
    sowStart = config.sowStart
    sowEnd = config.sowEnd
    
    # if sowStart is 'auto', set by location from provided lookup table
    if sowStart == 'auto':
        sowStart = gridLut['sow_start'][gridpoint]
    
    # if sowEnd is 'auto', set by location from provided lookup table
    if sowEnd == 'auto':
        sowEnd = gridLut['sow_end'][gridpoint]
    
    # end crop on fixed date rule
    # removes any crop that may be left in the groud 2 days before sowing
    endDate = datetime.strptime(sowStart, '%d-%b') - DateOffset(2)
    endDate = datetime.strftime(endDate, '%d-%b')
    manager.end_crop_on_fixed_date_rule(folder, crop, endDate)
        
    if crop == 'maize':
        # sowing rule
        if sowEnd == '':
            manager.sowOnFixedDate_rule(folder, crop,
                                                date=sowStart,\
                                                density=config.density,\
                                                depth=config.depth,\
                                                cultivar=config.cultivar,\
                                                gclass=config.gclass,\
                                                row_spacing=config.rowSpacing)
        else:
            manager.sowUsingAVariable_rule(folder, crop,
                                                   start_date=sowStart,\
                                                   end_date=sowEnd,\
                                                   density=config.density,\
                                                   depth=config.depth,\
                                                   cultivar=config.cultivar,\
                                                   gclass=config.gclass,\
                                                   row_spacing=config.rowSpacing)
    elif crop == 'cotton':
        # sowing rule
        if sowEnd == '':
            manager.cotton_fixed_date_sowing_rule(folder, crop,
                                                          date=sowStart)
        else:
            manager.cotton_sowing_rule(folder, crop,
                                               start_date=sowStart,\
                                               end_date=sowEnd)
    
    # add each shared rule to grid point
    for rulename, ruleType in rulesList:
        apsim.new_management_rule(folder, rulename, ruleType, shortcut)

def setup_graph_options(element):
    '''Sets up graphing options for all simulations.'''
    apsim.new_graph(element,'Date','yield')

def _new_shortcut(project, simulation, subfolder=''):
    '''Creates a new shortcut location.'''
    fullpath = '/' + project + '/' + simulation + '/' + subfolder
    return fullpath
    
def select_soil(gridpoint, crop, element, shortcutroot, soilLut, soilName):
    ''' Chooses soil to use based on grid cell.'''
    if soilName == 'auto':
        soilName = 'HCGEN' + str(soilLut[gridpoint]).zfill(4)
    shortcut = shortcutroot + soilName
    soil = apsim.new_soil(element, crop, soilName, shortcut)
    return soil

def new_apsim(outputFileDir, config):
    '''
    Creates a new apsim file in directory outputFileDir writing
    the metFileDir to each file.
    
    Parameters
    ----------
    outputFileDir : string
        path to save .apsim files to
    config : Config object from fileio module
        configuration settings for the run.
        
    Returns
    -------
    Name of the .apsim file which was saved to specified directory
    '''
    # set variables from config
    met = config.met
    crop = config.crop
    soilDataPath = config.soilDataPath # used to add soils to main
                                         # soil folder
    metFileDir = config.metFileDir
    
    # read grid lookup table
    gridLut = read_csv(config.gridLutPath, index_col='point_id')
    
    # begin creating .apsim xml
    projectName = met + '_' + crop
    doc = setup_project(projectName)
    soilfolder_name = 'Shared Soils'
    soilfolder = apsim.new_folder(doc, soilfolder_name)
    setup_soils(soilfolder, soilDataPath)
    managerSharedFolderName = 'Shared Management Rules'
    managerSharedFolder = apsim.new_folder(doc,managerSharedFolderName)
    rulesList = setup_shared_management_options(managerSharedFolder, crop, config)
    gridpointList = list(gridLut.index)
    
    # ---------------------
    # Setup base simulation
    # ---------------------
    gridpoint = gridpointList[0]
    simName_base = projectName + '_' + str(gridpoint).zfill(5)
    simulation = apsim.new_simulation(doc, simName_base)
    
    # met
    met_path_base = setup_met(met, metFileDir, gridpoint)
    apsim.new_metfile(simulation, met_path_base)
    
    # clock
    apsim.new_clock(simulation, config.clockStart, config.clockEnd)
    
    # summary file
    apsim.new_summaryfile(simulation, simName_base + '.sum')
    
    # paddock
    paddock_base = apsim.new_area(simulation)
    paddock_base_name = paddock_base.get('name')
    
    # soil
    soil = select_soil(gridpoint, crop, paddock_base,
                _new_shortcut(projectName, soilfolder.get('name')),\
                gridLut['soil_code'], config.soilName)
    
    # surface organic matter
    surfaceom_base = apsim.new_surfaceom(paddock_base, crop, 
                                         mass=config.mass,\
                                         cnr=config.cnr,\
                                         cpr=config.cpr,\
                                         standing_fraction=config.standingFraction)
    surfaceom_base_name = surfaceom_base.get('name')
    
    # irrigation
    irrigation_base = apsim.new_irrigation(paddock_base,
                                           automatic_irrigation=config.automaticIrrigation,\
                                           asw_depth=config.aswDepth,\
                                           crit_fr_asw=config.critFrAsw,\
                                           irrigation_efficiency=config.irrigationEfficiency,\
                                           irrigation_allocation=config.irrigationAllocation,\
                                           allocation=config.allocation,\
                                           default_no3_conc=config.defaultNo3Conc,\
                                           default_nh4_conc=config.defaultNh4Conc,\
                                           default_cl_conc=config.defaultClConc)
    irrigation_base_name = irrigation_base.get('name')
    
    # fertiliser
    apsim.new_fertiliser(paddock_base)
    
    # crop
    apsim.new_crop(paddock_base, crop)
    
    # management rules
    managerFolderName_base = 'Management Rules'
    managerFolder_base = apsim.new_folder(paddock_base, managerFolderName_base) 
    setup_management_options(managerFolder_base, crop, config, gridpoint, gridLut,
                _new_shortcut(projectName,managerSharedFolder.get('name')),\
                rulesList, soil)
    
    # output
    apsim.new_outputfile(paddock_base, config.outputVariables, config.outputEvents)
    
    # tracker
    apsim.new_tracker(paddock_base, config.trackerVariables)
    
    # graph
    #setup_graph_options(paddock_base)

    # ----------------------------------------------
    # Add simulations for the rest of the grid cells
    # ----------------------------------------------
    for gridpoint in gridpointList[1:]:
        simName = projectName + '_' + str(gridpoint).zfill(5)
        simulation = apsim.new_simulation(doc, simName)
        
        # met
        met_path = setup_met(met, metFileDir, gridpoint)
        apsim.new_metfile(simulation, met_path)
        
        # clock
        apsim.new_clock(simulation, shortcut=_new_shortcut(projectName,simName_base))
        
        # summary file
        apsim.new_summaryfile(simulation, simName + '.sum', _new_shortcut(projectName,simName_base))
        
        # paddock
        paddock = apsim.new_area(simulation, shortcut=_new_shortcut(projectName,simName_base,paddock_base_name))
        
        # soil
        soil = select_soil(gridpoint, crop, paddock, _new_shortcut(projectName, soilfolder_name), gridLut['soil_code'], config.soilName)
        
        # surface organic matter
        apsim.new_surfaceom(paddock, crop, shortcut=_new_shortcut(projectName,simName_base,paddock_base_name+'/'+surfaceom_base_name))
        
        # irrigation
        apsim.new_irrigation(paddock,shortcut=_new_shortcut(projectName,simName_base,paddock_base_name+'/'+irrigation_base_name))
        
        # fertiliser
        apsim.new_fertiliser(paddock, shortcut=_new_shortcut(projectName,simName_base,paddock_base_name))
        
        # crop
        apsim.new_crop(paddock, crop, shortcut=_new_shortcut(projectName,simName_base,paddock_base_name))
        
        # management rules
        managerFolderName = 'Management Rules'
        managerFolder = apsim.new_folder(paddock,managerFolderName) 
        setup_management_options(managerFolder, crop, config, gridpoint, gridLut,\
                                 _new_shortcut(projectName,managerSharedFolder.get('name')),\
                                rulesList, soil)
        
        # output
        apsim.new_outputfile(paddock, shortcut=_new_shortcut(projectName,simName_base,paddock_base_name))
        
        # tracker
        apsim.new_tracker(paddock, shortcut=_new_shortcut(projectName,simName_base,paddock_base_name))
        
        # graph
        #apsim.new_graph(paddock, shortcut=_new_shortcut(projectName,simName_base,paddock_base_name))
        
    apsimFilename = apsim.save_file(doc, projectName + '.apsim', outputFileDir)
    
    return apsimFilename