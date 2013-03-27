#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==============================================================================
# File input/output operations
#==============================================================================

import ConfigParser as configparser

def _clean(variables):
    '''
    Removes new line (\\n), return (\\r), tabs (\\t), and whitespace from variables.
    
    Parameters
    ----------
    variables : list
        list of text to clean
    
    Returns
    -------
    Cleaned text.
    '''
    cleaned = [v.replace('\n', '') for v in variables]
    cleaned = [v.replace('\t', '') for v in variables]
    cleaned = [v.replace('\r', '') for v in variables]
    cleaned = [v.strip() for v in variables]
    
    # remove empty variables
    cleaned = [v for v in cleaned if v != '']
    
    return cleaned

class Config:
    def __init__(self, configPath, section='apsimPreprocessor'):
        '''
        Reads config.ini file to initialize input parameters.
        
        Parameters
        ----------
        configPath : string
            path to configuration file
        section : string
            (optional) section name of configuration file where settings
            are located
        
        Returns
        -------
        Config object
        '''
        parser = configparser.SafeConfigParser()
        parser.read(configPath)
        
        # check to see if section exists
        if parser.has_section(section):
            # shared settings (in DEFAULT section)
            self._resolution = parser.get(section, 'resolution')
            self._gridLutPath = parser.get(section, 'gridLutPath')
            self._crop = parser.get(section, 'crop')
            self._met = parser.get(section, 'met')
            
            # data directories
            self._apsimModelDir = parser.get(section, 'apsimModelDir')
            self._metFileDir = parser.get(section, 'metFileDir')
            self._soilDataPath = parser.get(section, 'soilDataPath')
            
            # clock settings
            self._clockStart = parser.get(section, 'clock_start')
            self._clockEnd = parser.get(section, 'clock_end')
            
            # soil settings
            self._soilName = parser.get(section, 'soilName')
            
            # surface organic matter settings
            self._mass = parser.get(section, 'mass')
            self._cnr = parser.get(section, 'cnr')
            self._cpr = parser.get(section, 'cpr')
            self._standingFraction = parser.get(section, 'standing_fraction')
            
            # irrigation settings
            self._automaticIrrigation = parser.get(section, 'automatic_irrigation')
            self._aswDepth = parser.get(section, 'asw_depth')
            self._critFrAsw = parser.get(section, 'crit_fr_asw')
            self._irrigationEfficiency = parser.get(section, 'irrigation_efficiency')
            self._irrigationAllocation = parser.get(section, 'irrigation_allocation')
            self._allocation = parser.get(section, 'allocation')
            self._defaultNo3Conc = parser.get(section, 'default_no3_conc')
            self._defaultNh4Conc = parser.get(section, 'default_nh4_conc')
            self._defaultClConc = parser.get(section, 'default_cl_conc')
            
            # management rule: fertilizer settings
            self._fertAmtCriteria = parser.get(section, 'FertAmtCriteria')
            self._fertDepthCriteria = parser.get(section, 'FertDepthCriteria')
            self._fertDepth = parser.get(section, 'FertDepth')
            self._fertAmt = parser.get(section, 'FertAmt')
            self._fertType = parser.get(section, 'FertType')
            
            # management rule: sowing settings
            self._sowStart = parser.get(section, 'sow_start')
            self._sowEnd = parser.get(section, 'sow_end')
            self._density = parser.get(section, 'density')
            self._depth = parser.get(section, 'depth')
            self._cultivar = parser.get(section, 'cultivar')
            self._gclass = parser.get(section, 'class')
            self._rowSpacing = parser.get(section, 'row_spacing')
            
            # management rule: harvest settings
            self._harvestDate = parser.get(section, 'harvest_date')
            
            # output settings
            self._outputVariables = _clean(parser.get(section, 'outputVariables').split(','))
            self._outputEvents = _clean(parser.get(section, 'outputEvents').split(','))
            
            # tracker settings
            self._trackerVariables = _clean(parser.get(section, 'trackerVariables').split(','))
            
        else:
            print '*** Warning: section "{0}" does not exist'.format(section)
    
    # dictionary of items
    def toDict(self):
        return {# shared settings (in DEFAULT section)
                'resolution':self._resolution,
                'gridLutPath':self._gridLutPath,
                'crop':self._crop,
                'met':self._met,
                
                # data directories
                'apsimModelDir':self._apsimModelDir,
                'metFileDir':self._metFileDir,
                'soilDataPath':self._soilDataPath,
                
                # clock settings
                'clockStart':self._clockStart,
                'clockEnd':self._clockEnd,
                
                # soil settings
                'soilName':self._soilName,
                
                # surface organic matter settings
                'mass':self._mass,
                'cnr':self._cnr,
                'cpr':self._cpr,
                'standing_fraction':self._standingFraction,
                
                # irrigation settings
                'automatic_irrigation':self._automaticIrrigation,
                'asw_depth':self._aswDepth,
                'critFrAsw':self._critFrAsw,
                'irrigation_efficiency':self._irrigationEfficiency,
                'irrigation_allocation':self._irrigationAllocation,
                'allocation':self._allocation,
                'default_no3_conc':self._defaultNo3Conc,
                'default_nh4_conc':self._defaultNh4Conc,
                'default_cl_conc':self._defaultClConc,
                'FertAmtCriteria':self._fertAmt,
                
                # management rule: fertilizer settings
                'FertDepthCriteria':self._fertDepthCriteria,
                'FertDepth':self._fertDepth,
                'FertAmt':self._fertAmt,
                'FertType':self._fertType,
                
                # management rule: sowing settings
                'sowStart':self._sowStart,
                'sowEnd':self._sowEnd,
                'density':self._density,
                'depth':self._depth,
                'cultivar':self._cultivar,
                'class':self._gclass,
                'row_spacing':self._rowSpacing,
                
                # management rule: harvest settings
                'harvestDate':self._harvestDate,
                
                # output settings
                'outputVariables':self._outputVariables,
                'outputEvents':self._outputEvents,
                
                # tracker settings
                'trackerVariables':self._trackerVariables}
                
    # shared settings (in DEFAULT section)
    def resolution(self):
        return self._resolution
        
    def gridLutPath(self):
        return self._gridLutPath
        
    def crop(self):
        return self._crop
        
    def met(self):
        return self._met
        
    # data directories
    def apsimModelDir(self):
        return self._apsimModelDir
        
    def metFileDir(self):
        return self._metFileDir
    
    def soilDataPath(self):
        return self._soilDataPath
    
    # clock settings    
    def clockStart(self):
        return self._clockStart
    
    def clockEnd(self):
        return self._clockEnd
    
    # soil settings
    def soilName(self):
        return self._soilName
        
    # surface organic matter settings
    def mass(self):
        return self._mass
        
    def cnr(self):
        return self._cnr
        
    def cpr(self):
        return self._cpr
        
    def standingFraction(self):
        return self._standingFraction
        
    # irrigation settings
    def automaticIrrigation(self):
        return self._automaticIrrigation
        
    def aswDepth(self):
        return self._aswDepth
    
    def critFrAsw(self):
        return self._critFrAsw
    
    def irrigationEfficiency(self):
        return self._irrigationEfficiency
    
    def irrigationAllocation(self):
        return self._irrigationAllocation
        
    def allocation(self):
        return self._allocation
        
    def defaultNo3Conc(self):
        return self._defaultNo3Conc
        
    def defaultNh4Conc(self):
        return self._defaultNh4Conc
        
    def defaultClConc(self):
        return self._defaultClConc
    
    # management rule: fertilizer settings
    def fertAmtCriteria(self):
        return self._fertAmtCriteria
        
    def fertDepthCriteria(self):
        return self._fertDepthCriteria
        
    def fertDepth(self):
        return self._fertDepth
        
    def fertAmt(self):
        return self._fertAmt
        
    def fertType(self):
        return self._fertType
    
    # management rule: sowing settings
    def sowStart(self):
        return self._sowStart
    
    def sowEnd(self):
        return self._sowEnd
    
    def density(self):
        return self._density
        
    def depth(self):
        return self._depth
        
    def cultivar(self):
        return self._cultivar
        
    def gclass(self):
        return self._gclass
        
    def rowSpacing(self):
        return self._rowSpacing
    
    # management rule: harvest settings
    def harvestDate(self):
        return self._harvestDate
        
    # output settings
    def outputVariables(self):
        return self._outputVariables
        
    def outputEvents(self):
        return self._outputEvents
    
    # tracker settings
    def trackerVariables(self):
        return self._trackerVariables