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
        #print(soil.tag, '-', soil.get('name'), '-', soil.text)