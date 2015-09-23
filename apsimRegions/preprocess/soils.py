#!/usr/bin/env python
#==============================================================================
#     Module for parsing soil files
#==============================================================================

import lxml.etree as ET

def add_soils(element, filename):
    ''' Adds all soils in filename to element.
    
    Parameters
    ----------
    element : lxml element tree element
        element to add soils to
    filename : string
        filename to parse
    
    Returns
    -------
    Nothing
    '''
    
    soiltree = ET.parse(filename).getroot()
    for soil in soiltree:
        element.append(soil)
        #print(soil.tag, '-', soil.get('name'), '-', soil.text)  def __init__(self):


class InitialWater(object):
  def __init__(self):
    self.fractionFull = 0.8
    self.depthWetSoil = 'NaN'
    self.percetnMethod = 'FilledFromTop'
    self.relativeTo = 'll15'


class SoilCrop(SoilBase):
  def __init__(self):
    self.ll = [0.19327, 0.19327, 0.196545, 0.211165, 0.210638333333]
    self.kl = [0.08, 0.08, 0.08, 0.06, 0.05]
    self.xf = [1, 1, 1, 1, 1]


class Water(SoilBase):
  def __init__(self):
    self.bd = []
    self.airDry = [0.0644233333333, 0.19327, 0.196545, 0.211165, 0.210638333333]
    self.ll15 = []
    self.dul = []
    self.sat = [0.4156, 0.4156, 0.4247, 0.4108, 0.4098]
    self.soilCrop = SoilCrop()
    self.soilCrop.name = 'maize'


class SoilWater(SoilBase):
  def __init__(self):
    self.summerCona = 3
    self.summerU = 6
    self.summerDate = '1-Apr'
    self.winterCona = 2.5
    self.winterU = 9
    self.winterDate = '1-Nov'
    self.diffusConst = 58
    self.diffusSlope = 25
    self.salb = 0.13
    self.cn2Bare = 82
    self.cnRed = 20
    self.cnCov = 0.8
    self.slope = 'NaN'
    self.dischargeWidth = 'NaN'
    self.catchmentArea = 'NaN'
    self.maxPond = 'NaN'
    self.swcon = []


class SoilOrganicMatter(SoilBase):
  def __init__(self):
    self.rootCN = 45
    self.rootWt = 1000
    self.soilCN = 12.5
    self.enrACoeff = 7.4
    self.enrBCoeff = 0.2
    self.oc = []
    self.fBiom = []
    self.fInert = []
    self.ocUnits = 'Total'


class Analysis(SoilBase):
  def __init__(self):
    self.texture = ['Silty clay loam'] * 5
    self.munsellColour = ''
    self.ph = [6.739, 6.739, 6.554, 6.785, 6.79033333333]
    self.phUnits = 'Water'
    self.boronUnits = 'HotWater'


class Sample(SoilBase):
  def __init__(self):
    self.no3 = [0] * 5
    self.nh4 = [0] * 5
    self.no3Units = 'ppm'
    self.nh4Units = 'ppm'
    self.ocUnits = 'Volumetric'
    self.phUnits = 'Water'


class Soil(object):
  def __init__(self):
    self.name = ''
    self.recordNumber = 0
    self.latitude = 0
    self.longitude = 0
    self.yearOfSampling = 0
    self.initalWater = InitialWater()
    self.water = Water()
    self.water.bd = [1.5331734, 1.5331734, 1.50929955, 1.5457662, 1.5483897] # TODO: make dynamic 5
    self.water.ll15 = [0.19327, 0.19327, 0.196545, 0.211165, 0.210638333333] # TODO: make dynamic 7
    self.water.dul = [0.32025, 0.32025, 0.322485, 0.321115, 0.320948333333] # TODO: make dynamic 6
    self.soilWater = SoilWater()
    self.soilWater.swcon = [0.19, 0.15, 0.17, 0.22, 0.22]  # TODO: make dynamic 1
    self.soilOrganicMatter = SoilOrganicMatter()
    self.soilOrganicMatter.oc = [2.47354651163, 2.47354651163, 2.19840116279, 1.30770348837, 1.28580426357] # TODO: make dynamic 2
    self.soilOrganicMatter.fBiom = [0.035, 0.035, 0.024, 0.018, 0.01] # TODO: make dynamic 3
    self.soilOrganicMatter.fInert = [0.8, 0.82, 0.85, 0.95, 0.986] # TODO: make dynamic 4
    self.analysis = Analysis()
    self.sample = Sample()
