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


class InitialWater(object):
  def __init__(self):
    self.fractionFull = 0.8
    self.depthWetSoil = 'NaN'
    self.percentMethod = 'FilledFromTop'
    self.relativeTo = 'll15'


class SoilCrop(object):
  def __init__(self):
    self.name = 'maize'
    self.ll = [0.19327, 0.19327, 0.196545, 0.211165, 0.210638333333]
    self.kl = [0.08, 0.08, 0.08, 0.06, 0.05]
    self.xf = [1, 1, 1, 1, 1]


class Water(object):
  def __init__(self):
    self.bd = []
    self.airDry = [0.0644233333333, 0.19327, 0.196545, 0.211165, 0.210638333333]
    self.ll15 = []
    self.dul = []
    self.sat = [0.4156, 0.4156, 0.4247, 0.4108, 0.4098]
    self.soilCrop = SoilCrop()


class SoilWater(object):
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


class SoilOrganicMatter(object):
  def __init__(self):
    self.rootCN = 45
    self.rootWt = 1000
    self.soilCN = 12.5
    self.enrACoeff = 7.4
    self.enrBCoeff = 0.2
    self.oc = []
    self.fbiom = []
    self.finert = []
    self.ocUnits = 'Total'


class Analysis(object):
  def __init__(self):
    self.texture = ['Silty clay loam'] * 5
    self.munsellColour = ''
    self.ph = [6.739, 6.739, 6.554, 6.785, 6.79033333333]
    self.phUnits = 'Water'
    self.boronUnits = 'HotWater'


class Sample(object):
  def __init__(self):
    self.no3 = [0] * 5
    self.nh4 = [0] * 5
    self.no3Units = 'ppm'
    self.nh4Units = 'ppm'
    self.swUnits = 'Volumetric'
    self.ocUnits = 'Total'
    self.phUnits = 'Water'


class Soil(object):
  def __init__(self):
    self.name = ''
    self.thickness = []
    self.recordNumber = 0
    self.latitude = 0
    self.longitude = 0
    self.yearOfSampling = 0
    self.initalWater = InitialWater()
    self.water = Water()
    self.water.bd = []
    self.water.ll15 = []
    self.water.dul = []
    self.soilWater = SoilWater()
    self.soilWater.swcon = []
    self.soilOrganicMatter = SoilOrganicMatter()
    self.soilOrganicMatter.oc = []
    self.soilOrganicMatter.fbiom = []
    self.soilOrganicMatter.finert = []
    self.analysis = Analysis()
    self.sample = Sample()


def add_soil(element, soilDict):
  soil = Soil()
  soil.name = soilDict['name']
  soil.thickness = soilDict['thickness']
  soil.soilWater.swcon = soilDict['SWCON']
  soil.soilOrganicMatter.oc = soilDict['OC']
  soil.soilOrganicMatter.fbiom = soilDict['FBIOM']
  soil.soilOrganicMatter.finert = soilDict['FINERT']
  soil.water.bd = soilDict['BD']
  soil.water.dul = soilDict['DUL']
  soil.water.ll15 = soilDict['LL15']
  soil_et = ET.SubElement(element, 'Soil', name=soil.name)
  ET.SubElement(soil_et, 'RecordNumber').text = str(soil.recordNumber)
  ET.SubElement(soil_et, 'Latitude').text = str(soil.latitude)
  ET.SubElement(soil_et, 'Longitude').text = str(soil.longitude)
  ET.SubElement(soil_et, 'YearOfSampling').text = str(soil.yearOfSampling)

  init_water_et = ET.SubElement(soil_et, 'InitialWater', name='Initial water')
  ET.SubElement(init_water_et, 'FractionFull').text = str(soil.initalWater.fractionFull)
  ET.SubElement(init_water_et, 'DepthWetSoil').text = str(soil.initalWater.depthWetSoil)
  ET.SubElement(init_water_et, 'PercentMethod').text = str(soil.initalWater.percentMethod)
  ET.SubElement(init_water_et, 'RelativeTo').text = str(soil.initalWater.relativeTo)

  water_et = ET.SubElement(soil_et, 'Water')
  _layer_values(water_et, 'Thickness', soil.thickness)
  _layer_values(water_et, 'BD', soil.water.bd)
  _layer_values(water_et, 'AirDry', soil.water.airDry)
  _layer_values(water_et, 'LL15', soil.water.ll15)
  _layer_values(water_et, 'DUL', soil.water.dul)
  _layer_values(water_et, 'SAT', soil.water.sat)
  
  soil_crop_et = ET.SubElement(water_et, 'SoilCrop', name=soil.water.soilCrop.name)
  _layer_values(soil_crop_et, 'Thickness', soil.thickness)
  _layer_values(soil_crop_et, 'll', soil.water.soilCrop.ll)
  _layer_values(soil_crop_et, 'kl', soil.water.soilCrop.kl)
  _layer_values(soil_crop_et, 'xf', soil.water.soilCrop.xf)

  soil_water_et = ET.SubElement(soil_et, 'SoilWat')
  ET.SubElement(soil_water_et, 'SummerCona').text = str(soil.soilWater.summerCona)
  ET.SubElement(soil_water_et, 'SummerU').text = str(soil.soilWater.summerU)
  ET.SubElement(soil_water_et, 'SummerDate').text = soil.soilWater.summerDate
  ET.SubElement(soil_water_et, 'WinterCona').text = str(soil.soilWater.winterCona)
  ET.SubElement(soil_water_et, 'WinterU').text = str(soil.soilWater.winterU)
  ET.SubElement(soil_water_et, 'WinterDate').text = soil.soilWater.winterDate
  ET.SubElement(soil_water_et, 'DiffusConst').text = str(soil.soilWater.diffusConst)
  ET.SubElement(soil_water_et, 'DiffusSlope').text = str(soil.soilWater.diffusSlope)
  ET.SubElement(soil_water_et, 'Salb').text = str(soil.soilWater.salb)
  ET.SubElement(soil_water_et, 'CN2Bare').text = str(soil.soilWater.cn2Bare)
  ET.SubElement(soil_water_et, 'CNRed').text = str(soil.soilWater.cnRed)
  ET.SubElement(soil_water_et, 'Slope').text = soil.soilWater.slope
  ET.SubElement(soil_water_et, 'DischargeWidth').text = soil.soilWater.dischargeWidth
  ET.SubElement(soil_water_et, 'CatchmentArea').text = soil.soilWater.catchmentArea
  ET.SubElement(soil_water_et, 'MaxPond').text = soil.soilWater.maxPond
  _layer_values(soil_water_et, 'Thickness', soil.thickness)
  _layer_values(soil_water_et, 'SWCON', soil.soilWater.swcon)

  soil_om_et = ET.SubElement(soil_et, 'SoilOrganicMatter')
  ET.SubElement(soil_om_et, 'RootCN').text = str(soil.soilOrganicMatter.rootCN)
  ET.SubElement(soil_om_et, 'RootWt').text = str(soil.soilOrganicMatter.rootWt)
  ET.SubElement(soil_om_et, 'SoilCN').text = str(soil.soilOrganicMatter.soilCN)
  ET.SubElement(soil_om_et, 'EnrACoeff').text = str(soil.soilOrganicMatter.enrACoeff)
  ET.SubElement(soil_om_et, 'EnrBCoeff').text = str(soil.soilOrganicMatter.enrBCoeff)
  _layer_values(soil_om_et, 'Thickness', soil.thickness)
  _layer_values(soil_om_et, 'OC', soil.soilOrganicMatter.oc)
  _layer_values(soil_om_et, 'FBiom', soil.soilOrganicMatter.fbiom)
  _layer_values(soil_om_et, 'FInert', soil.soilOrganicMatter.finert)
  ET.SubElement(soil_om_et, 'OCUnits').text = str(soil.soilOrganicMatter.ocUnits)
  
  analysis_et = ET.SubElement(soil_et, 'Analysis')
  _layer_values(analysis_et, 'Thickness', soil.thickness)
  _layer_values(analysis_et, 'Texture', soil.analysis.texture)
  _layer_values(analysis_et, 'MunsellColour', soil.analysis.munsellColour)
  _layer_values(analysis_et, 'PH', soil.analysis.ph)
  ET.SubElement(soil_om_et, 'PHUnits').text = str(soil.analysis.phUnits)
  ET.SubElement(soil_om_et, 'BoronUnits').text = str(soil.analysis.boronUnits)

  sample_et = ET.SubElement(soil_et, 'Sample', name='Initial nitrogen')
  _layer_values(sample_et, 'Thickness', soil.thickness)
  _layer_values(sample_et, 'NO3', soil.sample.no3)
  _layer_values(sample_et, 'NH4', soil.sample.nh4)
  ET.SubElement(sample_et, 'NO3Units').text = soil.sample.no3Units
  ET.SubElement(sample_et, 'NH4Units').text = soil.sample.nh4Units
  ET.SubElement(sample_et, 'SWUnits').text = soil.sample.swUnits
  ET.SubElement(sample_et, 'OCUnits').text = soil.sample.ocUnits
  ET.SubElement(sample_et, 'PHUnits').text = soil.sample.phUnits


def _layer_values(element, name, layer_list, data_type='double'):
  layer_et = ET.SubElement(element, name)
  for layer in layer_list:
    ET.SubElement(layer_et, data_type).text = str(layer)


def main():
  from apsimRegions.preprocess.apsim import new_document, save_file
  doc = new_document(name='soils', version='36') # TODO: pull VERSION from to be made config.py as constant
  filename = 'soils.soils'
  outputFileDir = 'C:/Users/David/Documents/farmlogs'
  create_soils(doc, filename, outputFileDir)
  save_file(doc, filename, outputFileDir)


# Run main() if module is run as a program
if __name__ == '__main__':
  main()
