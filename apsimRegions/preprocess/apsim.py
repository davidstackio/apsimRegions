#!/usr/bin/env python
#==============================================================================
#     Module for creating an APSIM file. For use with APSIM v7.4. Basically
#     acts as a wrapper for APSIM.
# 
#     Import and call methods.
#
#     Created by David Stack (Chapman University - Orange, CA) on 1/26/2012
#==============================================================================

import os
import lxml.etree as ET

def new_document(version='', name=''):
    '''Creates a new root document. All inputs have to be strings.'''
    version = str(version)
    doc = ET.Element('folder', version=version, name=name)
    return doc

def new_simulation(doc, name=None, shortcut=None):
    '''Creates a new simulation.'''
    simulation = ET.SubElement(doc,'simulation', name=name)
    if shortcut != None:
        simulation = ET.SubElement(doc,'simulation', name=name, shortcut=shortcut)
    return simulation

def _new_filename(element, path=None):
    '''Creates new filename. Required for some elements.'''
    filename = ET.SubElement(element, 'filename', name='filename')
    filename.text = path
    return filename

def new_metfile(simulation, path, name='met', shortcut=None):
    '''Creates a new metfile.'''
    if shortcut == None:
        metfile = ET.SubElement(simulation, 'metfile', name=name)
        _new_filename(metfile, path)
    else:
        metfile = ET.SubElement(simulation, 'metfile', name=name, shortcut=shortcut)
    return metfile

def new_clock(simulation, start=None, end=None, shortcut=None):
    '''Creates a new clock.'''
    if shortcut == None:
        clock = ET.SubElement(simulation, 'clock')
        ET.SubElement(clock,'start_date', name='start_date', description='Enter the start date of the simulation', type='date').text = start
        ET.SubElement(clock,'end_date', name='end_date', description='Enter the end date of the simulation', type='date').text = end
    else:
        clock = ET.SubElement(simulation, 'clock', shortcut=shortcut+'clock')
    return clock

def new_summaryfile(simulation, path=None, shortcut=None):
    '''Creates a new summary file.'''
    if shortcut == None:
        summaryfile = ET.SubElement(simulation, 'summaryfile')
        _new_filename(summaryfile, path)
    else:
        summaryfile = ET.SubElement(simulation, 'summaryfile', shortcut=shortcut+'summaryfile')
    return summaryfile

def new_area(element, name='paddock', shortcut=None):
    '''Creates a new area, or paddock.'''
    if shortcut == None:
        area = ET.SubElement(element, 'area', name=name)
        # ET.SubElement(area, 'registrations', name='global')
    else:
        area = ET.SubElement(element, 'area', name=name, shortcut=shortcut)
    return area

def new_folder(element, name='', shortcut=None):
    '''Creates a new folder.'''
    if shortcut == None:
        folder = ET.SubElement(element, 'folder', name=name)
    else:
        folder = ET.SubElement(element, 'folder', name=name, shortcut=shortcut+'/'+name)
    return folder

def new_soil(element, crop, soilName=None, shortcut=None):
    '''Creates a new soil.'''
    if shortcut == None:
        soil = ET.SubElement(element, 'soil', name=soilName)
    else:
        soil = ET.SubElement(element, 'soil', name=soilName, shortcut=shortcut)
        ET.SubElement(soil, 'InitWater', name='Initial water', shortcut=shortcut+'/Initial water')

        water = ET.SubElement(soil, 'Water', shortcut=shortcut+'/Water')
        ET.SubElement(water, 'SoilCrop', name=crop, shortcut=shortcut+'/Water/'+crop)

        ET.SubElement(soil, 'SoilWat', shortcut=shortcut+'/SoilWat')
        ET.SubElement(soil, 'SoilOrganicMatter', shortcut=shortcut+'/SoilOrganicMatter')
        ET.SubElement(soil, 'Analysis', shortcut=shortcut+'/Analysis')
        ET.SubElement(soil, 'Sample', name='Initial nitrogen', shortcut=shortcut+'/Initial nitrogen')
        #ET.SubElement(soil, 'Phosphorus', name='Phosphorus', shortcut=shortcut+'/Phosphorus')        
    return soil

def new_management_rule(element, rulename, ruleType, shortcut):
    '''Creates a new managment rule shortcut to name.'''
    if ruleType == 'manager':
        rule = ET.SubElement(element, 'manager', name=rulename, shortcut=shortcut+rulename)
    elif ruleType == 'manager2':
        rule = ET.SubElement(element, 'manager2', name=rulename, shortcut=shortcut+rulename)
    else:
        print('Error: ruleType',ruleType,'does not exist.')
    return rule
    
def new_surfaceom(element, crop, name='surface organic matter', mass='1000.', cnr='80.0', cpr='', standing_fraction='0.0', shortcut=None):
    '''Creates a new surface organic matter.'''
    if shortcut == None:
        surfaceom = ET.SubElement(element, 'surfaceom', name=name)
        ET.SubElement(surfaceom, 'PoolName', type='text', description='Organic Matter pool name').text = crop
        ET.SubElement(surfaceom, 'type', type='list', listvalues='bambatsi,barley,base_type,broccoli,camaldulensis,canola,centro,chickpea,chikenmanure_base,cm,cmA,cmB,constants,cotton,cowpea,danthonia,fababean,fieldpea,fym,gbean,globulus,goatmanure,grandis,grass,horsegram,inert,lablab,lentil,lucerne,lupin,maize,manB,manure,medic,millet,mucuna,nativepasture,navybean,oats,orobanche,peanut,pigeonpea,potato,rice,sorghum,soybean,stylo,sugar,sunflower,sweetcorn,sweetsorghum,tillage,tithonia,vetch,weed,WF_Millet,wheat', description='Organic Matter type').text = crop
        ET.SubElement(surfaceom, 'mass', type='text', description='Initial surface residue (kg/ha)').text = mass
        ET.SubElement(surfaceom, 'cnr', type='text', description='C:N ratio of initial residue').text = cnr
        ET.SubElement(surfaceom, 'cpr', type='text', description='C:P ratio of initial residue (optional)').text = cpr
        ET.SubElement(surfaceom, 'standing_fraction', type='text', description='Fraction of residue standing').text = standing_fraction
    else:
        surfaceom = ET.SubElement(element, 'surfaceom', name=name, shortcut=shortcut)
    return surfaceom

def new_fertiliser(element, shortcut=None):
    '''Creates a new fertiliser.'''
    if shortcut == None:
        fertiliser = ET.SubElement(element, 'fertiliser')
    else:
        fertiliser = ET.SubElement(element, 'fertiliser', shortcut=shortcut+'/fertiliser')
    return fertiliser

def new_irrigation(element, name='Irrigation', automatic_irrigation='on', asw_depth='600', crit_fr_asw='0.5', irrigation_efficiency='1', irrigation_allocation='off', allocation='0', default_no3_conc='0.0', default_nh4_conc='0.0', default_cl_conc='0.0', shortcut=None):
    '''Creates a new irrigation.'''
    if shortcut == None:
        irrigation = ET.SubElement(element, 'irrigation', name=name)
        ET.SubElement(irrigation, 'automatic_irrigation', type='list', listvalues='on,off', description='Automatic irrigation').text = automatic_irrigation
        ET.SubElement(irrigation, 'asw_depth', type='text', description='Depth to which ASW is calculated. (mm)').text = asw_depth
        ET.SubElement(irrigation, 'crit_fr_asw', type='text', description='Fraction of ASW below which irrigation is applied (0-1.0)').text = crit_fr_asw        
        ET.SubElement(irrigation, 'irrigation_efficiency', type='text', description='Efficiency of the irrigation. (0-1.0)').text = irrigation_efficiency
        ET.SubElement(irrigation, 'irrigation_allocation', type='list', listvalues='on,off', description='Allocation limits').text = irrigation_allocation
        ET.SubElement(irrigation, 'allocation', type='text', description='Allocation in mm').text = allocation
        ET.SubElement(irrigation, 'default_no3_conc', type='text', description='Nitrate concentration (ppm N)').text = default_no3_conc
        ET.SubElement(irrigation, 'default_nh4_conc', type='text', description='Ammonium concentration (ppm N)').text = default_nh4_conc
        ET.SubElement(irrigation, 'default_cl_conc', type='text', description='Chloride concentration (ppm Cl)').text = default_cl_conc
    else:
        irrigation = ET.SubElement(element, 'irrigation', name=name, shortcut=shortcut)
    return irrigation
    
def new_crop(element, crop, shortcut=None):
    '''Creates a new crop.'''
    if shortcut == None:
        if crop == 'wheat':
            chosencrop = ET.SubElement(element, crop)
            chosencrop = _new_wheat(chosencrop)
        else:
            chosencrop = ET.SubElement(element, crop)
    else:
        chosencrop = ET.SubElement(element, crop, shortcut=shortcut+'/'+crop)
    return chosencrop

def _new_wheat(element, ModifyKL='yes'):
    wheat = ET.SubElement(element, 'ModifyKL', type = 'yesno', description = 'Modify KL using CL, EC or ESP if found?').text = ModifyKL
    return wheat

def new_outputfile(element, outputVariables=[], outputEvents=[], name_outputfile='outputfile', shortcut=None):
    '''Creates a new outputfile.'''
    if shortcut == None:
        outputfile = ET.SubElement(element, 'outputfile', name=name_outputfile)
        variables = ET.SubElement(outputfile, 'variables', name='Variables')
        for variable in outputVariables:
            ET.SubElement(variables, 'variable', name=variable)
        events = ET.SubElement(outputfile, 'events', name='Reporting Frequency')
        for event in outputEvents:
            ET.SubElement(events, 'event', name=event)
    else:
        outputfile = ET.SubElement(element, 'outputfile', name=name_outputfile, shortcut=shortcut+'/'+name_outputfile)
        variables = ET.SubElement(outputfile, 'variables', name='Variables', shortcut=shortcut+'/'+name_outputfile+'/Variables')
        events = ET.SubElement(outputfile, 'events', name='Reporting Frequency', shortcut=shortcut+'/'+name_outputfile+'/Reporting Frequency')
    return outputfile

def new_tracker(element, trackerVariables=[], name='tracker', shortcut=None):
    '''Creates a new tracker.'''
    if shortcut == None:
        tracker = ET.SubElement(element, 'tracker', name=name)
        for variable in trackerVariables:
            ET.SubElement(tracker, 'variable', name=variable)
    else:
        tracker = ET.SubElement(element, 'tracker', name=name, shortcut=shortcut+'/'+name)
    return tracker
    
def new_graph(element, plotX='x', plotY='y', name='XY', seriestype='Solid line', pointtype='Circle', color=None, shortcut=None):
    '''Creates a new graph.'''
    if shortcut == None:
        graph = ET.SubElement(element, 'graph', name=name)
        Plot = ET.SubElement(graph, 'Plot')
        ET.SubElement(Plot, 'SeriesType').text = seriestype
        ET.SubElement(Plot, 'PointType').text = pointtype
        ET.SubElement(Plot, 'colour').text = color
        ET.SubElement(Plot, 'X').text = plotX
        ET.SubElement(Plot, 'Y').text = plotY
        ET.SubElement(Plot, 'GDApsimFileReader', name='GDApsimFileReader')
    else:
        graph = ET.SubElement(element, 'graph', name=name, shortcut=shortcut+'/'+name)
        Plot = ET.SubElement(graph, 'Plot', shortcut=shortcut+'/'+name+'/Plot')
        ET.SubElement(Plot, 'GDApsimFileReader', name='GDApsimFileReader', shortcut=shortcut+'/'+name+'/Plot/GDApsimFileReader')
    return graph

def save_file(doc, filename, outputFileDir):
    '''Generates pretty apsim xml and saves file.'''
    saveLocation = os.path.join(outputFileDir,filename)
    with open(saveLocation, 'wb') as f:
        xmlpretty = ET.tostring(doc, pretty_print=True, encoding='UTF-8')
        f.write(xmlpretty)
    return filename