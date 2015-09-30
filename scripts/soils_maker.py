#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apsimRegions.preprocess.apsim import new_document, save_file
from apsimRegions.preprocess.soils import add_soil

def main():
  doc = new_document(name='soils', version='36') # TODO: pull VERSION from to be made config.py as constant
  filename = 'soils.soils'
  outputFileDir = 'C:/Users/Username/Documents/exampleProject'
  soilDict = {
        'name': 'control',
        'thickness': [100, 100, 300, 500, 1000],
        'SWCON': [0.19, 0.15, 0.17, 0.22, 0.22],
        'OC': [2.47354651163, 2.47354651163, 2.19840116279, 1.30770348837, 1.28580426357],
        'FBIOM': [0.035, 0.035, 0.024, 0.018, 0.01],
        'FINERT': [0.8, 0.82, 0.85, 0.95, 0.986],
        'BD': [1.5331734, 1.5331734, 1.50929955, 1.5457662, 1.5483897],
        'DUL': [0.32025, 0.32025, 0.322485, 0.321115, 0.320948333333],
        'LL15': [0.19327, 0.19327, 0.196545, 0.211165, 0.210638333333],
    }
  add_soil(doc, soilDict)
  save_file(doc, filename, outputFileDir)


# Run main() if module is run as a program
if __name__ == '__main__':
  main()
