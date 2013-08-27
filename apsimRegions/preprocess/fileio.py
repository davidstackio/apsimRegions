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
            self.resolution = parser.get(section, 'resolution')
            self.gridLutPath = parser.get(section, 'gridLutPath')
            self.crop = parser.get(section, 'crop')
            self.met = parser.get(section, 'met')
            
            # data directories
            self.apsimModelDir = parser.get(section, 'apsimModelDir')
            self.metFileDir = parser.get(section, 'metFileDir')
            self.soilDataPath = parser.get(section, 'soilDataPath')
            
            # clock settings
            self.clockStart = parser.get(section, 'clock_start')
            self.clockEnd = parser.get(section, 'clock_end')
            
            # soil settings
            self.soilName = parser.get(section, 'soilName')
            
            # surface organic matter settings
            self.mass = parser.get(section, 'mass')
            self.cnr = parser.get(section, 'cnr')
            self.cpr = parser.get(section, 'cpr')
            self.standingFraction = parser.get(section, 'standing_fraction')
            
            # irrigation settings
            self.automaticIrrigation = parser.get(section, 'automatic_irrigation')
            self.aswDepth = parser.get(section, 'asw_depth')
            self.critFrAsw = parser.get(section, 'crit_fr_asw')
            self.irrigationEfficiency = parser.get(section, 'irrigation_efficiency')
            self.irrigationAllocation = parser.get(section, 'irrigation_allocation')
            self.allocation = parser.get(section, 'allocation')
            self.defaultNo3Conc = parser.get(section, 'default_no3_conc')
            self.defaultNh4Conc = parser.get(section, 'default_nh4_conc')
            self.defaultClConc = parser.get(section, 'default_cl_conc')
            
            # management rule: fertilizer settings
            self.fertAmtCriteria = parser.get(section, 'FertAmtCriteria')
            self.fertDepthCriteria = parser.get(section, 'FertDepthCriteria')
            self.fertDepth = parser.get(section, 'FertDepth')
            self.fertAmt = parser.get(section, 'FertAmt')
            self.fertType = parser.get(section, 'FertType')
            
            # management rule: sowing settings
            self.sowStart = parser.get(section, 'sow_start')
            self.sowEnd = parser.get(section, 'sow_end')
            self.density = parser.get(section, 'density')
            self.depth = parser.get(section, 'depth')
            self.cultivar = parser.get(section, 'cultivar')
            self.gclass = parser.get(section, 'class')
            self.rowSpacing = parser.get(section, 'row_spacing')
            
            # management rule: harvest settings
            self.harvestDate = parser.get(section, 'harvest_date')
            
            # output settings
            self.outputVariables = _clean(parser.get(section, 'outputVariables').split(','))
            self.outputEvents = _clean(parser.get(section, 'outputEvents').split(','))
            
            # tracker settings
            self.trackerVariables = _clean(parser.get(section, 'trackerVariables').split(','))
            
        else:
            print '*** Warning: section "{0}" does not exist'.format(section)
    
    # dictionary of items
    def toDict(self):
        return self.__dict__
                
#    # shared settings (in DEFAULT section)
#    def resolution(self):
#        return self._resolution
#        
#    def gridLutPath(self):
#        return self._gridLutPath
#        
#    def crop(self):
#        return self._crop
#        
#    def met(self):
#        return self._met
#        
#    # data directories
#    def apsimModelDir(self):
#        return self._apsimModelDir
#        
#    def metFileDir(self):
#        return self._metFileDir
#    
#    def soilDataPath(self):
#        return self._soilDataPath
#    
#    # clock settings    
#    def clockStart(self):
#        return self._clockStart
#    
#    def clockEnd(self):
#        return self._clockEnd
#    
#    # soil settings
#    def soilName(self):
#        return self._soilName
#        
#    # surface organic matter settings
#    def mass(self):
#        return self._mass
#        
#    def cnr(self):
#        return self._cnr
#        
#    def cpr(self):
#        return self._cpr
#        
#    def standingFraction(self):
#        return self._standingFraction
#        
#    # irrigation settings
#    def automaticIrrigation(self):
#        return self._automaticIrrigation
#        
#    def aswDepth(self):
#        return self._aswDepth
#    
#    def critFrAsw(self):
#        return self._critFrAsw
#    
#    def irrigationEfficiency(self):
#        return self._irrigationEfficiency
#    
#    def irrigationAllocation(self):
#        return self._irrigationAllocation
#        
#    def allocation(self):
#        return self._allocation
#        
#    def defaultNo3Conc(self):
#        return self._defaultNo3Conc
#        
#    def defaultNh4Conc(self):
#        return self._defaultNh4Conc
#        
#    def defaultClConc(self):
#        return self._defaultClConc
#    
#    # management rule: fertilizer settings
#    def fertAmtCriteria(self):
#        return self._fertAmtCriteria
#        
#    def fertDepthCriteria(self):
#        return self._fertDepthCriteria
#        
#    def fertDepth(self):
#        return self._fertDepth
#        
#    def fertAmt(self):
#        return self._fertAmt
#        
#    def fertType(self):
#        return self._fertType
#    
#    # management rule: sowing settings
#    def sowStart(self):
#        return self._sowStart
#    
#    def sowEnd(self):
#        return self._sowEnd
#    
#    def density(self):
#        return self._density
#        
#    def depth(self):
#        return self._depth
#        
#    def cultivar(self):
#        return self._cultivar
#        
#    def gclass(self):
#        return self._gclass
#        
#    def rowSpacing(self):
#        return self._rowSpacing
#    
#    # management rule: harvest settings
#    def harvestDate(self):
#        return self._harvestDate
#        
#    # output settings
#    def outputVariables(self):
#        return self._outputVariables
#        
#    def outputEvents(self):
#        return self._outputEvents
#    
#    # tracker settings
#    def trackerVariables(self):
#        return self._trackerVariables