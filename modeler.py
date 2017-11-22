import json
import math
import csv
import collections

with open('inputs.json') as f:
  data = json.load(f)

class Surface:
  def __init__(self, surfaceName):
    self.amc = 0  # antecedent moisture condition g/sf
    self.duration =                data['general']['intervalMins'] # minutes
    self.rainIntensityIncrement =  data['general']['rainIntensityIncrement']  # g/sf/min, 0.0007, 0.0014, 0.0021
    self.rainIntensityIncrements = data['general']['rainIntensityIncrements'] # 8 from 0.0007 to 0.0056
    self.vwcIncrement =            data['general']['vwcIncrement'] # integer 0-100 (usually 5)

    self.controlledLo = 0      # vwc (integer 0-100)
    self.controlledHi = 70     # vwc (integer 0-100)
    self.controlledRate = 0.05 # g/sf/min
    
    self.surfaceName =  surfaceName
    self.surface =      data['surfaces'][self.surfaceName] # key of product in array
    self.runoffToName = self.surface['runoff']
    self.etTableName =  self.surface['etTable'] # which et table to use for this surface's exposure, # is array index
    self.productName =  self.surface['product']  # key of product in array

    self.product =      data['products'][self.productName]  # key of product in array
    self.capacity =     self.product['capacityGsf']   # g/sf
    self.type =         self.product['type']
    
    if self.etTableName != None:
      self.etTable =    data['et'][self.etTableName]  # key of product in array
    else:
      self.etTable =    None

    self.runoff = 0

    self.month = 1
    self.minutes = 0
    self.minsDay = 24 * 60
    self.minsMonth = 30.5 * self.minsDay
    self.minsEtColumn = 120
    self.output = []

    self.idHeaderTitle = [
      'surfaceName',
      '',
      'productName',
    ]
    self.idHeader = [
      self.surfaceName,
      '',
      self.productName,
    ]
    self.initializeHeaderTitle = [
      'Duration',
      '','',
      'capacity',
      'vwcIncrement',
      '','',
      'rainIntensityIncrement',
      'rainIntensityIncrements',
      '',
      'controlledRate',
      'controlledLo',
      'controlledHi',
      '',
      'runoffToName',
      '','',
      'etTableName',
      'minsEtColumn'
    ]
    self.initializeHeader = [
      self.duration,
      '','',
      self.capacity,
      self.vwcIncrement,
      '','',
      self.rainIntensityIncrement,
      self.rainIntensityIncrements,
      '',
      self.controlledRate,
      self.controlledLo,
      self.controlledHi,
      '',    
      self.runoffToName,
      '','',
      self.etTableName,
      self.minsEtColumn
    ]
    self.outputHeader = [
      'month',
      'minutes',

      'amc',
      'vwc',
      'vwcGroupBy5',
      'vwcRow',
      'capacitySpare',

      'rainIntensity',
      'intensityColumn' ,
      'rain',
      'uncontrolled',
      'controlled',
      'input',
  
      'efficiency',
      'absorb',
      'runoff',
      'retPre',
        
      'hourColumn',
      'etRate',
      'etMax',
      'et',

      'ret'
    ]

  def cycle(self, rainIntensity, uncontrolled): # rain, uncontrolled are volume in gals/sf/minute

    # calculate capacity at start of cycle
    capacitySpare = self.capacity - self.amc
    vwc = int((self.amc / self.capacity) * 100 )
    vwcGroupBy5 = int(vwc/self.vwcIncrement) * self.vwcIncrement
    vwcRow =  int(vwc/self.vwcIncrement)

    # rain, uncontrolled cannot be negative numbers
    self.rain = rainIntensity * self.duration
    
    intensityColumn = int(rainIntensity/self.rainIntensityIncrement) + 1 # start at 1, not 0
    if intensityColumn > self.rainIntensityIncrements - 1:
      intensityColumn = self.rainIntensityIncrements - 1

    efficiency = self.product['efficiency'][vwcRow][intensityColumn]

    # calculate controlled inputs, factor in weather later
    if self.rain > 0 or uncontrolled > 0: # no controlled release during rain
      self.controlled = 0
    elif (vwc < self.controlledLo) or (vwc > self.controlledHi): # no controlled release outside vwc parameters
      self.controlled = 0
    elif (self.controlledRate * self.duration) > capacitySpare: # no controlled release if it would put us over capacity
      self.controlled = 0
    else:
      self.controlled = self.controlledRate * self.duration

    self.input = self.rain + uncontrolled + self.controlled

    if self.input <= capacitySpare:
      self.absorb = self.input * efficiency/100
    # if input > capacity, absorb to capacity, rest runs off (add eff. factor later)
    else:
      self.absorb = 0

    self.runoff = self.input - self.absorb
    retPre = self.amc + self.absorb
    
    hourColumn = int( (self.minutes %  self.minsDay) / self.minsEtColumn ) # calc which 2-hour column we are in
    etRate = self.etTable['table'][self.month][hourColumn] # gal/sf/min
    etMax = etRate * self.duration # gal/sf/min
    # no ET during rain
    if self.rain > 0:
      et = 0
    elif etMax > retPre:
      et = retPre  # ET cannot exceed retention... improve this... as vwc drops, et is more difficult to extract
    else:
      et = etMax

    self.ret = retPre - et

    self.output = [
      self.month,
      self.minutes,

      self.amc,
      vwc,
      vwcGroupBy5,
      vwcRow,
      capacitySpare,

      rainIntensity,
      intensityColumn,
      self.rain,
      uncontrolled,
      self.controlled,
      self.input,
  
      efficiency,
      self.absorb,
      self.runoff,
      retPre,
        
      hourColumn,
      etRate,
      etMax,
      et,

      self.ret
    ]

    self.minutes += self.duration
    self.month = int(self.minutes/self.minsMonth)+1
    self.amc = self.ret

  def receive(self, uncontrolled): # uncontrolled volume in gals/sf/minute
    
    capacitySpare = self.capacity - self.amc

    self.input = uncontrolled
    
    self.absorb = self.input

    self.runoff = self.input - self.absorb
    self.ret = self.amc + self.absorb
    
    self.output = [
      self.month,
      self.minutes,
      self.amc,
      '','','',
      capacitySpare,
      '','','',
      uncontrolled,
      '',
      self.input,
      '',
      self.absorb,
      self.runoff,
      '','','','','',
      self.ret
    ]

    self.minutes += self.duration
    self.month = int(self.minutes/self.minsMonth)+1
    self.input = uncontrolled

    # calculate capacity at start of cycle
    capacitySpare = self.capacity - self.amc
    vwc = int((self.amc / self.capacity) * 100 )

# create a loop
# accumulate total rain
# create Cistern class to use for controlled release, accumulate release (can get into negative numbers for now)
# create Offsite class to contain runoff, accumulate runoff

# create and populate dictionary
surfaces = {}
rainTable = data['events']['rainIntensity']

for surface in data['surfaces']:
  surfaces[surface] = Surface(surface)

# add header to file for each surface
for surface in surfaces:
  filename = surface + 'Model.csv'
  with open(filename, 'w', newline='') as csvfile:
    modelwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    modelwriter.writerow(surfaces[surface].idHeaderTitle)
    modelwriter.writerow(surfaces[surface].idHeader)
    modelwriter.writerow([])
    modelwriter.writerow(surfaces[surface].initializeHeaderTitle)
    modelwriter.writerow(surfaces[surface].initializeHeader)
    modelwriter.writerow([])
    modelwriter.writerow(surfaces[surface].outputHeader)

# cycle through each surface for each event in rainTable; order doesn't matter, as long as all cycles 1 occur before all cycles 2, etc.
for event in rainTable:
  runoff = collections.defaultdict(int)
  for surface in surfaces:
    filename = surface + 'Model.csv'
    if surfaces[surface].type != 'receiving':
      surfaces[surface].cycle(event,runoff[surface])
      runoff[surfaces[surface].runoffToName] += surfaces[surface].runoff
    else:
      surfaces[surface].receive(runoff[surface])
    with open(filename, 'a', newline='') as csvfile:
      modelwriter = csv.writer(csvfile, delimiter=',',
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
      display = ["%.4f" % x if isinstance(x, float) else x for x in surfaces[surface].output]
      modelwriter.writerow(display)

