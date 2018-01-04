import json
import math
import csv
import collections
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import time # used for runtime only

with open('inputs.json') as f:
  data = json.load(f)

class Event:
  def __init__(self, surface):
    self.surfaceName = surface.surfaceName
    self.eventNum = surface.eventNum

    self.rain =         surface.eventTotalRain
    self.uncontrolled = surface.eventTotalUncontrolled
    self.controlled =   surface.eventTotalControlled
    self.absorb =       surface.eventTotalAbsorb
    self.runoff =       surface.eventTotalRunoff
    self.et =           surface.eventTotalEt
    
    self.start =        surface.eventStart
    self.retStart =     surface.eventRetStart
    self.stop =         surface.eventStop
    self.retStop =      surface.eventRetStop
    self.threshold =    surface.eventThreshold
    self.retThreshold = surface.eventRetThreshold
    self.end =          surface.eventEnd
    self.retEnd =       surface.eventRetEnd

  def formatEventSummaries(self):
    # add more here related to analysis
    self.input = self.rain + self.uncontrolled + self.controlled
    pctAbsorbed = self.absorb / self.input
    pctRunoff = self.runoff / self.input
    pctEt = self.et / self.input

    retDeltaRain = self.retStop - self.retStart
    minsDeltaRain = self.stop - self.start
    retRateRain = retDeltaRain / minsDeltaRain

    retDeltaInitDry = self.retStop - self.retThreshold
    minsDeltaInitDry = self.threshold - self.stop
    retRateInitDry = retDeltaInitDry / minsDeltaInitDry

    retDeltaLaterDry = self.retThreshold - self.retEnd
    minsDeltaLaterDry = self.end - self.threshold
    retRateLaterDry = retDeltaLaterDry / minsDeltaLaterDry

    rainRate = self.rain / minsDeltaRain
    duration = self.end - self.start

    self.eventSummaryHeader = [
      'surfaceName', 
      'eventNum',
      'duration',
      'rain',
      'rainRate',
      'uncontrolled',
      'controlled',
      'input',
      'absorb',
      'pctAbsorbed',
      'runoff',
      'pctRunoff',
      'et',
      'pctEt',

      'start',
      'retStart',

      'retDeltaRain',
      'minsDeltaRain',
      'retRateRain',

      'stop',
      'retStop',

      'retDeltaInitDry',
      'minsDeltaInitDry',
      'retRateInitDry',

      'threshold',
      'retThreshold',

      'retDeltaLaterDry',
      'minsDeltaLaterDry',
      'retRateLaterDry',

      'end',
      'retEnd'
    ]
    self.eventSummary = [
      self.surfaceName, 
      self.eventNum,
      duration,
      self.rain,
      rainRate,
      self.uncontrolled,
      self.controlled,
      self.input,
      self.absorb,
      pctAbsorbed,
      self.runoff,
      pctRunoff,
      self.et,
      pctEt,

      self.start,
      self.retStart,

      retDeltaRain,
      minsDeltaRain,
      retRateRain,

      self.stop,
      self.retStop,

      retDeltaInitDry,
      minsDeltaInitDry,
      retRateInitDry,

      self.threshold,
      self.retThreshold,

      retDeltaLaterDry,
      minsDeltaLaterDry,
      retRateLaterDry,

      self.end,
      self.retEnd

    ]


class Surface:
  def __init__(self, surfaceName):
    self.amc = 0  # antecedent moisture condition g/sf
    self.duration =                data['general']['intervalMins'] # minutes
    self.eventStopThreshold =  int(data['general']['eventGapThreshold']/self.duration) # integer of minimum minutes between rain events; e.g. 480 = 8 hours
    self.rainIntensityIncrement =  data['general']['rainIntensityIncrement']  # g/sf/min, 0.0007, 0.0014, 0.0021
    self.rainIntensityIncrements = data['general']['rainIntensityIncrements'] # 8 from 0.0007 to 0.0056
    self.vwcIncrementEff =         data['general']['vwcIncrementEff'] # integer 0-100 (usually 5)
    self.vwcIncrementEt =          data['general']['vwcIncrementEt'] # integer 0-100 (usually 10)

    self.controlledRate =          data['general']['controlledRate'] # volume per minute
    self.controlledLo =            data['general']['controlledLo'] # vwc (integer 0-100)
    self.controlledHi =            data['general']['controlledHi'] # vwc (integer 0-100)
    
    self.surfaceName =  surfaceName
    self.surface =      data['surfaces'][self.surfaceName] # key of product in list
    self.runoffToName = self.surface['runoff']
    self.etTableName =  self.surface['etTable']  # which et table to use for this surface's exposure, # is list index
    self.productName =  self.surface['product']  # key of product in list
    self.area =         self.surface['area']     # units of area, integer, e.g. 5000

    self.product =      data['products'][self.productName] # key of product in list
    self.capacity =     self.product['capacity'] # volume per 1 unit of area 
    self.type =         self.product['type']
    
    if self.etTableName != None:
      self.etTable =    data['et'][self.etTableName] # key of product in list
    else:
      self.etTable =    None

    self.runoff = 0

    self.month = 1
    self.minutes = 0
    self.minsDay = 24 * 60
    self.minsMonth = 30.5 * self.minsDay
    self.minsEtColumn = 120

    self.rain = 0
    self.rainTotal = 0
    self.controlled = 0
    self.controlledTotal = 0
    self.uncontrolledTotal = 0
    self.inputTotal = 0
    self.absorbTotal = 0
    self.runoffTotal = 0
    self.et = 0
    self.etTotal = 0
    self.lossesTotal = 0

    self.cycles = 0 # counts # of cycles
    self.cyclesPerGraphOutput = 1 # 5 = combine 5 cycles into 1 output

    self.eaListRain = [] # these lists capture 'each' increment, e.g. each rain input over 1 cycle
    self.eaListUncontrolled = []
    self.eaListControlled = []
    self.eaListAbsorb = []
    self.eaListRunoff = []
    self.eaListEt = []

    self.totListRet = []  # the totLists capture running totals, e.g. total cumulative rain; these reset at each rain event

    self.totListRain = []
    self.totListUncontrolled = []
    self.totListControlled = []
    self.totListAbsorb = []
    self.totListRunoff = []
    self.totListEt = []

    self.eventStopCounter = 0
    self.eventStatus = 'dry'
    self.eventNum = 0

    self.eventTotalRain = 0
    self.eventTotalUncontrolled = 0
    self.eventTotalControlled = 0
    self.eventTotalAbsorb = 0
    self.eventTotalRunoff = 0
    self.eventTotalEt = 0
    
    self.eventThreshold = 0
    self.eventRetStop = 0
    self.eventRetThreshold = 0

    self.eventStart = 0
    self.eventRetStart = 0
    self.eventEnd = None
    self.eventRetEnd = None

    self.events = {}

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
      'duration',
      'area',
      '','',
      'vwcIncrementEff',
      '',
      'capacity',
      'rainIntensityIncrement',
      'rainIntensityIncrements',
      '',
      'controlledRate',
      'controlledLo',
      'controlledHi',
      '','','',
      'runoffToName',
      '','',
      'etTableName',
      'vwcIncrementEt',
      'minsEtColumn'
    ]
    self.initializeHeader = [
      self.duration,
      self.area,
      '','',
      self.vwcIncrementEff,
      '',
      self.capacity,
      self.rainIntensityIncrement,
      self.rainIntensityIncrements,
      '',
      self.controlledRate,
      self.controlledLo,
      self.controlledHi,
      '','','',
      self.runoffToName,
      '','',
      self.etTableName,
      self.vwcIncrementEt,
      self.minsEtColumn
    ]
    self.outputHeader = [
      'month',
      'minutes',

      'amc',
      'vwc',
      'vwcGroupEff',
      'vwcRowEff',
      'capacitySpare',

      'rainIntensity',
      'intensityColumn' ,
      'rain',
      'uncontrolledRawVol',
      'uncontrolled',
      'controlled',
      'input',
  
      'efficiency',
      'absorb',
      'runoff',
      'runoffRawVol',
      'retPre',
      
      'vwcGroupEt',
      'vwcRowEt',
      'hourColumn',
      'etRate',
      'etMax',
      'et',

      'ret',

      'rainTotal',
      'controlledTotal',
      'uncontrolledTotal',
      'inputTotal',
      'runoffTotal',
      'etTotal',
      'lossesTotal',
    ]

  def cycle(self, rainIntensity, uncontrolledRawVol): # rain, uncontrolled are volume in gals/sf/minute

    # calculate capacity at start of cycle
    capacitySpare = self.capacity - self.amc
    vwc = int((self.amc / self.capacity) * 100 )
    vwcGroupEff = int(vwc/self.vwcIncrementEff) * self.vwcIncrementEff
    vwcRowEff =   int(vwc/self.vwcIncrementEff)
    vwcGroupEt =  int(vwc/self.vwcIncrementEt)  * self.vwcIncrementEt
    vwcRowEt =    int(vwc/self.vwcIncrementEt)
    # calculate uncontrolled inputs (rain, uncontrolled); neither can be negative numbers
    self.rain = rainIntensity * self.duration
    self.uncontrolledRawVol = uncontrolledRawVol
    self.uncontrolled = self.uncontrolledRawVol / self.area

    # calculate controlled inputs, factor in weather later
    if self.rain > 0 or self.uncontrolled > 0: # no controlled release during rain
      self.controlled = 0
    elif (vwc < self.controlledLo) or (vwc > self.controlledHi): # no controlled release outside vwc parameters
      self.controlled = 0
    elif (self.controlledRate * self.duration) > capacitySpare: # no controlled release if it would put us over capacity
      self.controlled = 0
    else:
      self.controlled = self.controlledRate * self.duration

    self.input = self.rain + self.uncontrolled + self.controlled

    # calculate efficiency of absorption
    intensityColumn = int(rainIntensity/self.rainIntensityIncrement) + 1 # start at 1, not 0
    if intensityColumn > self.rainIntensityIncrements - 1:
      intensityColumn = self.rainIntensityIncrements - 1
    efficiency = self.product['efficiency'][vwcRowEff][intensityColumn]

    # calculate absorption
    if self.input <= capacitySpare:
      self.absorb = self.input * efficiency/100
    else:
      self.absorb = 0

    # calculate runoff
    self.runoff = self.input - self.absorb
    self.runoffRawVol = self.runoff * self.area
    retPre = self.amc + self.absorb
    
    # calculate ET
    hourColumn = int( (self.minutes %  self.minsDay) / self.minsEtColumn ) # calc which 2-hour column we are in
    # print('month, hour', self.month, hourColumn)
    etRate = self.etTable['table'][self.month][vwcRowEt][hourColumn] # gal/sf/min
    etMax = etRate * self.duration # gal/sf/min
    # no ET during rain
    if self.rain > 0:
      self.et = 0
    elif etMax > retPre:
      self.et = retPre  # ET cannot exceed retention... improve this... as vwc drops, et is more difficult to extract
    else:
      self.et = etMax

    # finalize retention this cycle
    self.ret = retPre - self.et

    # output for csv
    self.output = [
      self.month,
      self.minutes,

      self.amc,
      vwc,
      vwcGroupEff,
      vwcRowEff,
      capacitySpare,

      rainIntensity,
      intensityColumn,
      self.rain,
      self.uncontrolledRawVol,
      self.uncontrolled,
      self.controlled,
      self.input,
  
      efficiency,
      self.absorb,
      self.runoff,
      self.runoffRawVol,
      retPre,
        
      vwcGroupEt,
      vwcRowEt,
      hourColumn,
      etRate,
      etMax,
      self.et,

      self.ret,

      self.rainTotal,
      self.controlledTotal,
      self.uncontrolledTotal,
      self.inputTotal,
      self.runoffTotal,
      self.etTotal,
      self.lossesTotal
    ]

    # enumerate rain events, accumulate totals per events, reset totals to 0 when events change
    self.eventCalcs()
    # output for graph
    self.populateGraphLists()
    # increment for next cycle
    self.increment()

  def receive(self, uncontrolledRawVol): # uncontrolled volume in gals/sf/minute
    self.uncontrolledRawVol = uncontrolledRawVol
    self.uncontrolled = uncontrolledRawVol
    
    capacitySpare = self.capacity - self.amc
    self.input = self.uncontrolled
    self.absorb = self.input
    self.runoff = self.input - self.absorb
    self.runoffRawVol = self.runoff
    self.ret = self.amc + self.absorb
    
    self.output = [
      self.month,
      self.minutes,
      self.amc,
      '','','',
      capacitySpare,
      '','','',
      self.uncontrolledRawVol,
      '','',
      self.input,
      '',
      self.absorb,
      self.runoff,
      self.runoffRawVol,
      '','','','','','','',
      self.ret,
      '','',
      self.uncontrolledTotal,
      self.inputTotal,
      self.runoffTotal,
      '',
      self.lossesTotal
    ]
    # enumerate rain events, accumulate totals per events, reset totals to 0 when events change
    self.eventCalcs()
    # output for graph
    self.populateGraphLists()
    # increment for next cycle
    self.increment()

  def captureEventTotals(self):
    # save the prior event as an object in the events dictionary
    self.eventEnd = self.minutes
    self.eventRetEnd = self.ret
    eventNameNum = self.surfaceName + str(self.eventNum)
    if self.eventNum > 0:
      self.events[eventNameNum] = Event(self)
  
  def resetEventTotals(self):
    self.eventTotalRain = self.rain
    self.eventTotalUncontrolled = self.uncontrolled
    self.eventTotalControlled = self.controlled
    self.eventTotalAbsorb = self.absorb
    self.eventTotalRunoff = self.runoff
    self.eventTotalEt = self.et

    self.eventStart = self.minutes
    self.eventRetStart = self.ret
    self.eventStop = None
    self.eventRetStop = None
    self.eventThreshold = None  
    self.eventRetThreshold = None
    self.eventEnd = None
    self.eventRetEnd = None

  def incrementEventTotals(self):
    self.eventTotalRain += self.rain
    self.eventTotalUncontrolled += self.uncontrolled
    self.eventTotalControlled += self.controlled
    self.eventTotalAbsorb += self.absorb
    self.eventTotalRunoff += self.runoff
    self.eventTotalEt += self.et
  
  def eventCalcs(self):
    if self.rain > 0:
      if self.eventStatus == 'dry': # just started raining
        self.eventTotalStop = self.minutes - self.duration
        self.captureEventTotals()
        self.resetEventTotals()
        self.eventNum += 1
      else:                         # if 'stop' or if keeps raining
        self.incrementEventTotals()
      self.eventStatus = 'rain'
      self.eventStop = self.minutes
      self.eventRetStop = self.ret
      self.eventStopCounter = 0
    # no rain below here
    elif self.eventStatus == 'stop':
      if self.eventStopCounter >= self.eventStopThreshold: 
        self.eventStopCounter = 0                     # has stopped, just met threshold
        self.eventStatus = 'dry'
        self.eventThreshold = self.minutes
        self.eventRetThreshold = self.ret

      if self.eventStopCounter >= 0:                   # recently stopped
        self.eventStopCounter += self.duration 
      self.incrementEventTotals()
    
    elif self.eventStatus == 'rain':                # just stopped raining
      self.eventStopCounter = 0
      self.eventStatus = 'stop'
      self.eventStop = self.minutes
      self.eventRetStop = self.ret
      self.incrementEventTotals()
    else:
      self.eventStopCounter = 0                     # been dry longer than threshold
      self.eventStatus = 'dry'
      self.incrementEventTotals()

  def increment(self):
    self.minutes += self.duration
    self.month = int(self.minutes/self.minsMonth)+1 # fix this to cycle or add cycler

    self.amc = self.ret

    self.rainTotal += self.rain
    self.controlledTotal += self.controlled
    self.uncontrolledTotal += self.uncontrolled
    self.inputTotal += self.input
    self.absorbTotal += self.absorb
    self.runoffTotal += self.runoff
    self.etTotal += self.et
    self.lossesTotal = self.runoffTotal + self.etTotal

  def populateGraphLists(self):
    self.eaListRain.append(self.rain)
    self.eaListUncontrolled.append(self.uncontrolled)
    self.eaListControlled.append(self.controlled)
    self.eaListAbsorb.append(self.absorb)
    self.eaListRunoff.append(self.runoff)
    self.eaListEt.append(self.et)

    self.totListRet.append(self.ret)

    self.totListRain.append(self.eventTotalRain)
    self.totListUncontrolled.append(self.eventTotalUncontrolled)
    self.totListControlled.append(self.eventTotalControlled)
    self.totListAbsorb.append(self.eventTotalAbsorb)
    self.totListRunoff.append(self.eventTotalRunoff)
    self.totListEt.append(self.eventTotalEt)

  def outputGraphs(self):
    filename = self.surfaceName + 'Graph.png'

    time = np.arange(len(self.eaListRain))
    # pass thru data now, later might aggregate into fewer points
    ret =          self.totListRet

    rain =         self.totListRain
    uncontrolled = self.totListUncontrolled
    controlled =   self.totListControlled
    absorb =       self.totListAbsorb
    runoff =       self.totListRunoff
    et =           self.totListEt

    fig, ax = plt.subplots() # ax = plt.subplots()[1] instead of fix... investigate...
    ax.plot(time,rain, 'C1',label='rain') # x,y
    ax.plot(time,uncontrolled, 'C2',label='uncontrolled')
    ax.plot(time,controlled, 'C3',label='controlled')
    ax.plot(time,absorb, 'C4',label='absorb')
    ax.plot(time,runoff, 'C5',label='runoff')
    ax.plot(time,et, 'C6',label='et')
    ax.plot(time,ret, 'C7',label='ret')

    legend = ax.legend(loc='upper center', shadow=True)

    plt.xlabel('time')
    plt.ylabel('volume', multialignment='center')
    plt.grid(True)

    plt.savefig(filename)

  def outputEventTables(self):
    filename = self.surfaceName + 'Events.csv'
    with open(filename, 'w') as csvfile:
      eventwriter = csv.writer(csvfile, delimiter=',',
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
      counter = 0
      for event in self.events:
        self.events[event].formatEventSummaries()
        counter += 1
        if counter == 1:
          eventwriter.writerow(self.events[event].eventSummaryHeader)
        eventwriter.writerow(self.events[event].eventSummary)

# start time
startTime = time.time()
# create and populate dictionary
surfaces = {}
rainTable = data['events']['rainIntensity']

for surface in data['surfaces']:
  surfaces[surface] = Surface(surface)

# add header to file for each surface
for surface in surfaces:
  filename = surface + 'Model.csv'
  with open(filename, 'w') as csvfile:
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
      runoff[surfaces[surface].runoffToName] += surfaces[surface].runoffRawVol
    else:
      surfaces[surface].receive(runoff[surface])
    with open(filename, 'a') as csvfile:
      modelwriter = csv.writer(csvfile, delimiter=',',
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
      display = ["%.4f" % x if isinstance(x, float) else x for x in surfaces[surface].output]
      modelwriter.writerow(display)
  for surface in surfaces:
    surfaces[surface].captureEventTotals() # captures the final event

for surface in surfaces:
  surfaces[surface].outputGraphs()
  surfaces[surface].outputEventTables()

print('The script took {0} seconds!'.format(time.time() - startTime))