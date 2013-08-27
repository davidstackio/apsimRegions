#!/usr/bin/env python
#==============================================================================
# Module that contains all management rules.
#==============================================================================

import lxml.etree as ET

def sowOnFixedDate_rule(folder,crop,name='Sow on a fixed date',shortcut=None,date='1-jan',density='10',depth='50',cultivar='',gclass='plant',row_spacing='500',occurrence='start_of_day'):
    ''' Rule for sowing on fixed date.'''
    
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)
        
        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description='Sowing criteria')
        ET.SubElement(ui, 'date', type='text', description='Enter sowing date (dd-mmm) : ').text = date
        
        ET.SubElement(ui, 'category', type='category', description='Sowing parameters')
        ET.SubElement(ui, 'crop', type='crop', description='Enter name of crop to sow : ').text = crop
        ET.SubElement(ui, 'density', type='text', description='Enter sowing density (plants/m2) : ').text = density
        ET.SubElement(ui, 'depth', type='text', description = 'Enter sowing depth (mm) : ').text = depth
        ET.SubElement(ui, 'cultivar', type='cultivars', description='Enter cultivar : ').text = cultivar
        ET.SubElement(ui, 'class', type='classes', description='Enter crop growth class : ').text = gclass
        ET.SubElement(ui, 'row_spacing', type='text', description='Enter row spacing (mm) : ').text = row_spacing
        
        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
      if (today = date('[date]') then
              [crop] sow plants =[density], sowing_depth = [depth], cultivar = [cultivar], row_spacing = [row_spacing], crop_class = [class]
         endif
      '''
        ET.SubElement(script, 'event').text = occurrence
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule
    
def sowUsingAVariable_rule(folder,crop,name='Sow using a variable rule',shortcut=None,start_date='',end_date='',must_sow='yes',raincrit='30',rainnumdays='3',esw_amount='200',density='3',depth='50',cultivar='usa_18leaf',gclass='plant',row_spacing='250',occurrence='start_of_day'):
    ''' Rule for sowing on a variable date.'''
    
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)

        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description='Sowing criteria')
        ET.SubElement(ui, 'date1', type='ddmmmdate', description='Enter sowing window START date (dd-mmm) : ').text = start_date
        ET.SubElement(ui, 'date2', type='ddmmmdate', description='Enter sowing window END date (dd-mmm) : ').text = end_date
        ET.SubElement(ui, 'must_sow', type='yesno', description='Must sow? : ').text = must_sow
        ET.SubElement(ui, 'raincrit', type='text', description='Amount of rainfall : ').text = raincrit
        ET.SubElement(ui, 'rainnumdays', type='text', description='Number of days of rainfall : ').text = rainnumdays
        ET.SubElement(ui, 'esw_amount', type='text', description='Enter minimum allowable available soil water (mm) : ').text = esw_amount
        
        ET.SubElement(ui, 'category', type='category', description='Sowing parameters')
        ET.SubElement(ui, 'crop', type='crop', description='Enter name of crop to sow : ').text = crop
        ET.SubElement(ui, 'density', type='text', description='Enter sowing density (plants/m2) : ').text = density
        ET.SubElement(ui, 'depth', type='text', description = 'Enter sowing depth (mm) : ').text = depth
        ET.SubElement(ui, 'cultivar', type='cultivars', description='Enter cultivar : ').text = cultivar
        ET.SubElement(ui, 'class', type='classes', description='Enter crop growth class : ').text = gclass
        ET.SubElement(ui, 'row_spacing', type='text', description='Enter row spacing (mm) : ').text = row_spacing

        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
      if (paddock_is_fallow() = 1 and FallowIn <> 'yes' and (NextCrop = 0 or NextCrop = '[crop]')) then
         if (date_within('[date1], [date2]') = 1) then
            if (rain[[rainnumdays]] >= [raincrit] AND esw >= [esw_amount]) OR
                ('[must_sow]' = 'yes' AND today = date('[date2]'))) THEN
               ChooseNextCrop = 'yes'   ! for rotations
               [crop] sow plants =[density], sowing_depth = [depth], cultivar = [cultivar], row_spacing = [row_spacing], crop_class = [class]
            endif
            if today = date('[date2]') then
               ChooseNextCrop = 'yes'
            endif
         endif
      endif
      '''
        ET.SubElement(script, 'event').text = occurrence
        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
        nextcrop = 0
        fallowin = 0
        '''
        ET.SubElement(script, 'event').text = 'init'
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule

def cotton_sowing_rule(folder,crop,name='Cotton sowing rule',shortcut=None,start_date='',end_date='',must_sow='yes',raincrit='30',rainnumdays='3',esw_amount='200',density='10',depth='30',cultivar='siok',row_spacing='1000',skiprow='0',occurrence='start_of_day'):
    ''' Rule for sowing cotton in a date range.'''
    
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)

        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description='Sowing criteria')
        ET.SubElement(ui, 'date1', type='ddmmmdate', description='Enter sowing window START date (dd-mmm) : ').text = start_date
        ET.SubElement(ui, 'date2', type='ddmmmdate', description='Enter sowing window END date (dd-mmm) : ').text = end_date
        ET.SubElement(ui, 'must_sow', type='yesno', description='Must sow? : ').text = must_sow
        ET.SubElement(ui, 'raincrit', type='text', description='Amount of rainfall : ').text = raincrit
        ET.SubElement(ui, 'rainnumdays', type='text', description='Number of days of rainfall : ').text = rainnumdays
        ET.SubElement(ui, 'esw_amount', type='text', description='Enter minimum allowable available soil water (mm) : ').text = esw_amount
        
        ET.SubElement(ui, 'category', type='category', description='Sowing parameters')
        ET.SubElement(ui, 'crop', type='crop', description='Enter name of crop to sow : ').text = crop
        ET.SubElement(ui, 'density', type='text', description='Enter sowing density (plants/m2) : ').text = density
        ET.SubElement(ui, 'depth', type='text', description = 'Enter sowing depth (mm) : ').text = depth
        ET.SubElement(ui, 'cultivar', type='cultivars', description='Enter cultivar : ').text = cultivar
        ET.SubElement(ui, 'row_spacing', type='text', description='Enter row spacing (mm) : ').text = row_spacing
        ET.SubElement(ui, 'skiprow', type='list', listvalues='0,1,2', description='Skip row : ').text = skiprow

        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
      if (paddock_is_fallow() = 1 and FallowIn <> 'yes' and (NextCrop = 0 or NextCrop = '[crop]')) then
         if (date_within('[date1], [date2]') = 1) then
            if (rain[[rainnumdays]] >= [raincrit] AND esw >= [esw_amount]) OR
                ('[must_sow]' = 'yes' AND today = date('[date2]'))) THEN
               ChooseNextCrop = 'yes'   ! for rotations
               [crop] sow plants_pm =[density], sowing_depth = [depth], cultivar = [cultivar], row_spacing = [row_spacing], skiprow = [skiprow]
            endif
            if today = date('[date2]') then
               ChooseNextCrop = 'yes'
            endif
         endif
      endif
      '''
        ET.SubElement(script, 'event').text = occurrence
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule

def cotton_fixed_date_sowing_rule(folder,crop,name='Cotton fixed date sowing rule',shortcut=None,date='',density='10',depth='30',cultivar='siok',row_spacing='1000',occurrence='start_of_day'):
    ''' Rule for sowing cotton on a fixed date.'''
    
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)

        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description='Sowing criteria')
        ET.SubElement(ui, 'date', type='text', description='Enter sowing date (dd-mmm) : ').text = date
        
        ET.SubElement(ui, 'category', type='category', description='Sowing parameters')
        ET.SubElement(ui, 'crop', type='crop', description='Enter name of crop to sow : ').text = crop
        ET.SubElement(ui, 'density', type='text', description='Enter sowing density (plants/m2) : ').text = density
        ET.SubElement(ui, 'depth', type='text', description = 'Enter sowing depth (mm) : ').text = depth
        ET.SubElement(ui, 'cultivar', type='cultivars', description='Enter cultivar : ').text = cultivar
        ET.SubElement(ui, 'row_spacing', type='text', description='Enter row spacing (mm) : ').text = row_spacing

        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
      if (today = date('[date]') then
              [crop] sow plants_pm =[density], sowing_depth = [depth], cultivar = [cultivar], row_spacing = [row_spacing]
         endif
      '''
        ET.SubElement(script, 'event').text = occurrence
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule
    
def sowingFertiliser_rule(folder, name='Sowing fertiliser', shortcut=None, eventname='sowing', fertiliser='fertiliser', fert_amount_sow='150', fert_type_sow='urea_N'):
    '''Rule for when to apply fertilizer.'''
    
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)

        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description='When should fertiliser be applied')
        ET.SubElement(ui, 'eventname', type='text', description='On which event should fertiliser be applied : ').text = eventname
        ET.SubElement(ui, 'category', type='category', description='Fertiliser application details')
        ET.SubElement(ui, 'fertmodule', type='modulename', description='Module used to apply the fertiliser : ').text = fertiliser
        ET.SubElement(ui, 'fert_amount_sow', type='text', description='Amount of starter fertiliser at sowing (kg/ha) : ').text = fert_amount_sow
        ET.SubElement(ui, 'fert_type_sow', type='list', listvalues='NO3_N, NH4_N, NH4NO3, urea_N, urea_no3, urea, nh4so4_n, rock_p, banded_p, broadcast_p', description='Sowing fertiliser type : ').text = fert_type_sow

        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
        [fertmodule] apply amount = [fert_amount_sow] (kg/ha), depth = 50 (mm), type = [fert_type_sow]
        '''
        ET.SubElement(script, 'event').text = '[modulename].[eventname]'
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule

def harvesting_rule(folder, crop, name='Harvesting rule', shortcut=None):
    ''' Rule for when to harvest the crop.'''
    
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)

        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description='Harvesting criteria')
        ET.SubElement(ui, 'crop', type='text', description='Enter name of crop to harvest when ripe : ').text = crop

        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
           if ('[crop]' = 'cotton') then
              if ([crop].ozcot_status > 0) then
                  [crop] harvest
              endif
           elseif ([crop].StageName = 'harvest_ripe' or [crop].plant_status = 'dead') then
              [crop]  harvest
              [crop]  end_crop
           endif
           '''
        ET.SubElement(script, 'event').text = 'end_of_day'
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule

def end_crop_on_fixed_date_rule(folder, crop, harvestDate='1-jan', name='End crop on a fixed date', shortcut=None):
    '''
    Rule for ending a crop on a fixed date.
    
    Parameters
    ----------
    folder : element tree object
        node to attach rule to
    crop : string
        crop to harvest
    harvestDate : string (dd-mmm)
        (optional) date to harvest crop
    name : string
        (optional) name of component to display in APSIM gui
    shortcut : string
        (optional) shortcut to link to
        
    Returns
    -------
    The management rule.
    '''
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)

        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description='Harvesting criteria')
        ET.SubElement(ui, 'crop', type='crop', description='Enter name of crop to harvest when ripe : ').text = crop
        ET.SubElement(ui, 'date', type='text', description='Enter ending date (dd-mmm) : ').text = harvestDate

        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
           if (today = date('[date]') then
              [crop]  end_crop
           endif
           '''
        ET.SubElement(script, 'event').text = 'end_of_day'
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule
    
def irrigate_on_sw_deficit_rule(folder, name='irrigate at sw deficit', shortcut=None, trigger='50', occurrence='start_of_day'):
    ''' Rule for when to irrigate, and under what conditions.'''
    
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)

        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'trigger', type='text', description='Enter sw deficit to irrigate at (mm)').text = trigger

        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
           '''
        ET.SubElement(script, 'event').text = 'init'
        
        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
        if sw_dep() > [trigger] then        
            irrigation apply amount = [trigger]
            endif
           '''
        ET.SubElement(script, 'event').text = occurrence
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule
    
def fertOnSoilNCriteria_rule(folder, name='FertOnSoilNCriteria', shortcut=None, FertAmtCriteria='50', FertDepthCriteria='75', FertDepth='50', FertAmt='25', FertType='urea_n'):
    ''' Rule for when to apply fertilizer with Manager 2.'''
    
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager2', name=name)
        
        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description="Test for the mineral N in the soil and don't apply the fertiliser if greater than X kgN/ha is stored in the soil above a depth of Y mm")
        ET.SubElement(ui, 'FertAmtCriteria', type='text', description="Don't add fertiliser if N in the soil to the depth below exceeds (kg/ha)").text = FertAmtCriteria
        ET.SubElement(ui, 'FertDepthCriteria', type='text', description="Depth to which the amount of N in the soil should be calculated (mm)").text = FertDepthCriteria
        ET.SubElement(ui, 'category', type='category', description="Fertiliser application details")
        ET.SubElement(ui, 'FertDepth', type='text', description="Depth at which to apply the fertiliser (mm)").text = FertDepth
        ET.SubElement(ui, 'FertAmt', type='text', description="Amount of fertiliser to add (kg N /ha)").text = FertAmt
        ET.SubElement(ui, 'FertType', type='list', listvalues="no3_n,nh4_n,nh4no3,urea_n,urea_no3,urea,nh4so4_n,rock_p,banded_p,broadcast_p", description="Fertiliser type - select from the list").text = FertType
        
        ET.SubElement(rule, 'text').text = '''Imports System
Imports ModelFramework

Public Class Script 
   <Link()> Dim MyPaddock As Paddock
   <Link()> Dim Fert As Fertiliser
   
   'Parameters - user inputs from the Properties tab
   <Param> Private FertAmtCriteria As Single    'Don't apply fertiliser if the N stored in the soil is greater than this.  Disregard the test if the value is -ve
   <Param> Private FertDepthCriteria As Single  'Depth in the soil to calculate the N storage
   <Param> Private FertDepth As Single          'Depth in the soil that the fertilser will be applied
   <Param> Private FertAmt As Single            'Total annual application - needs to be split up between the various application dates listed
   <Param> Private FertType As String           'Type of fertliser to apply
   
   'Inputs - got by this Manager from elsewhere in APSIM
   <Input> Private Today As DateTime            'Today's date from APSIM 
   <Input> Private dlayer As Single()           'Array of soil layer thicknesses - for calculation of mineral N in the soil
   <Input> Private no3 As Single()              'Array of nitrate-N (kg N /ha) for each soil layer - for calculation of mineral N in the soil
   <Input> Private nh4 As Single()              'Array of ammonium-N (kg N /ha) for each soil layer - for calculation of mineral N in the soil
   <Input> Private urea As Single()             'Array of urea-N (kg N /ha) for each soil layer - for calculation of mineral N in the soil

   'Outputs - calculated by this Manager and available to be output by the user
   <Output> Private CumSoilN As Single          'Mineral-N stored in the soil to a depth of FertDepthCriteria

   'Other variables that are calculated but not needed for outputs
   Private LayerWeights As Single()             'Weigthing of each layer for FertAmtCriteria calculation


   <EventHandler()> Public Sub OnInit2()
      '"OnInit2" is an event handler gets called once at the start of the simulation 

      'nothing to do in here

   End Sub
   
   <EventHandler()> Public Sub OnPrepare()
      '"OnPrepare" is an event handler gets called once at the start of every day (before Prepare and Post) 
      
      'Set the number of elements in the LayerWeights array to equal the number of soil layers - do this here because erosion can change the layering
      'Then move through the array and assign a LayerWeighting from 0 to 1 quantifying what proportion of the soil and mineral N in this layer is above FertDepthCriteria
      ReDim LayerWeights(dlayer.length - 1)                
      Dim CumDepth As Single = 0.0
         For i As Integer = 0 To dlayer.Length - 1     
            CumDepth += dlayer(i)                      
         If CumDepth <= FertDepthCriteria Then
            LayerWeights(i) = 1.0                   
         ElseIf (CumDepth - dlayer(i)) <= FertDepthCriteria Then
            LayerWeights(i) = (FertDepthCriteria - (CumDepth - dlayer(i))) / dlayer(i)
         Else
            LayerWeights(i) = 0.0
         End If
      Next

      'Add up the no3, nh4 and urea (all already in kg N /ha) in each layer and multiply by the layer weighting to get the total mineral N to the set depth
      CumSoilN = 0.0
      For i As Integer = 0 To dlayer.Length - 1     
         CumSoilN += (no3(i) + nh4(i) + urea(i)) * LayerWeights(i)                         
      Next

      'If there is less mineral N in the soil than FertAmtCriteria then it is OK to add fertiliser
      '"Fert.Apply" send the command to apply the specified amount of fertiliser at the specified depth of the specified type of fertiliser
      If CumSoilN <= FertAmtCriteria Then
         Fert.Apply(FertAmt, FertDepth, FertType)
      End If

   End Sub

End Class
'''
    else:
        rule = ET.SubElement(folder, 'manager2', name=name, shortcut=shortcut+'/'+name)
    return rule

def reset_on_fixed_date(folder, crop, soilmodule, reset_date, name='Reset water, nitrogen and surfaceOM on fixed date', shortcut=None, surfaceommodule='surface organic matter', resetWater='yes', resetNitrogen='yes', resetSurfaceOM='yes', occurrence='start_of_day'):
    '''
    Resets water, nitrogen, and surfaceOM on a fixed date.
    
    Parameters
    ----------
    
    Returns
    -------
    The management rule.
    '''
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)
        
        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description="When should a reset be done")
        ET.SubElement(ui, 'reset_date', type='ddmmdate', description="Enter date of reset (dd-mmm)").text = reset_date
        ET.SubElement(ui, 'category', type='category', description="Reset details")
        ET.SubElement(ui, 'soilmodule', type='modulename', description="Name of your soil module : ").text = soilmodule
        ET.SubElement(ui, 'surfaceommodule', type='modulename', description="Name of your surface organic matter module : ").text = surfaceommodule
        ET.SubElement(ui, 'resetWater', type='yesno', description="Reset soil water?").text = resetWater
        ET.SubElement(ui, 'resetNitrogen', type='yesno', description="Reset soil nitrogen?").text = resetNitrogen
        ET.SubElement(ui, 'resetSurfaceOM', type='yesno', description="Reset surface organic matter?").text = resetSurfaceOM
        
        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
           if (today = date('[reset_date]')) then
            resetWater = '[resetWater]'
            resetNitrogen  = '[resetNitrogen]'
            resetSurfaceOM = '[resetSurfaceOM]'
            if (resetWater = 'yes') then
                '[soilmodule] Water' reset
            endif
            if (resetNitrogen = 'yes') then
                '[soilmodule] Nitrogen' reset
            endif
            if (resetSurfaceOM = 'yes') then
                '[surfaceommodule]' reset
            endif
            act_mods reseting
         endif
           '''
        ET.SubElement(script, 'event').text = occurrence
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule

def reset_on_sowing(folder, crop, soilmodule, name='Reset water, nitrogen and surfaceOM on sowing', shortcut=None, surfaceommodule='surface organic matter', resetWater='yes', resetNitrogen='yes', resetSurfaceOM='yes', eventname='sowing'):
    '''
    Resets water, nitrogen, and surfaceOM on sowing.
    
    Parameters
    ----------
    
    Returns
    -------
    The management rule.
    '''
    if shortcut == None:
        rule = ET.SubElement(folder, 'manager', name=name)
        
        ui = ET.SubElement(rule, 'ui')
        ET.SubElement(ui, 'category', type='category', description="When should a reset be done")
        ET.SubElement(ui, 'modulename', type='modulename', description="The module the event is to come from : ").text = crop
        ET.SubElement(ui, 'eventname', type='text', description="On which event should a reset be done : ").text = eventname
        ET.SubElement(ui, 'category', type='category', description="Reset details")
        ET.SubElement(ui, 'soilmodule', type='modulename', description="Name of your soil module : ").text = soilmodule
        ET.SubElement(ui, 'surfaceommodule', type='modulename', description="Name of your surface organic matter module : ").text = surfaceommodule
        ET.SubElement(ui, 'resetWater', type='yesno', description="Reset soil water?").text = resetWater
        ET.SubElement(ui, 'resetNitrogen', type='yesno', description="Reset soil nitrogen?").text = resetNitrogen
        ET.SubElement(ui, 'resetSurfaceOM', type='yesno', description="Reset surface organic matter?").text = resetSurfaceOM
        
        script = ET.SubElement(rule, 'script')
        ET.SubElement(script, 'text').text = '''
            resetWater = '[resetWater]'
            resetNitrogen  = '[resetNitrogen]'
            resetSurfaceOM = '[resetSurfaceOM]'
            if (resetWater = 'yes') then
                '[soilmodule] Water' reset
            endif
            if (resetNitrogen = 'yes') then
                '[soilmodule] Nitrogen' reset
            endif
            if (resetSurfaceOM = 'yes') then
                '[surfaceommodule]' reset
            endif
            if (resetWater = 'yes' or resetNitrogen = 'yes' or resetSurfaceOM = 'yes') then
               act_mods reseting
            endif
           '''
        ET.SubElement(script, 'event').text = '[modulename].[eventname]'
    else:
        rule = ET.SubElement(folder, 'manager', name=name, shortcut=shortcut+'/'+name)
    return rule