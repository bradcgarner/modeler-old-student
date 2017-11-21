import json
import math
# that is like require(express)

with open('inputs.json') as f:
  data = json.load(f)


class Surface:
  def __init__(self, duration,rainIntensityIncrement,rainIntensityIncrements,vwcIncrement,surface):
    self.amc = 0  # antecedent moisture condition g/sf
    self.duration = duration # minutes
    self.rainIntensityIncrement = rainIntensityIncrement # g/sf/min, 0.0007, 0.0014, 0.0021
    self.rainIntensityIncrements = rainIntensityIncrements # g/sf/min, 0.0007, 0.0014, 0.0021
    self.vwcIncrement = vwcIncrement # integer 0-100 (usually 5)

    self.controlledLo = 0      # vwc (integer 0-100)
    self.controlledHi = 70     # vwc (integer 0-100)
    self.controlledRate = 0.05 # g/sf/min
    
    self.surface =     data['surfaces'][surface] # key of product in array
    self.runoffTo =    self.surface['runoff']
    self.cda =         self.surface['cda']    # contributing drainage area, i.e. uncontrolled runoff from
    self.etTableName = self.surface['etTable'] # which et table to use for this surface's exposure, # is array index
    self.productName = self.surface['product']  # key of product in array

    self.product =     data['products'][self.productName]  # key of product in array
    self.capacity =    self.product['capacityGsf']   # g/sf
    
    self.etTable =     data['et'][self.etTableName]  # key of product in array

    self.runoff = 0

    self.month = 1
    self.minutes = 0
    self.minsDay = 24 * 60
    self.minsMonth = 30.5 * self.minsDay
    self.minsEtSlot = 120

  def cycle(self, rainIntensity, uncontrolled):
    # rain, uncontrolled are volume in gals/sf/minute

    print(' ')
    print('INITIALIZE')
    print('duration = 5: ',self.duration)
    print('capacity g/sf = 0.50 ',self.capacity)
    print('rainIntensityIncrement = 0.0007 ',rainIntensityIncrement)
    print('vwcIncrement = 5: ',self.vwcIncrement)
    print('runoffTo: ',self.runoffTo)
    print('cda: ',self.cda)
    print('controlledLo: ',  self.controlledLo)
    print('controlledHi: ',  self.controlledHi)
    print('controlledRate: ',self.controlledRate)
    print('month: ',self.month)
    print('minutes: ',self.minutes)
    print('minsMonth: ',self.minsMonth)
    print('etTable:', self.etTable)

    # calculate capacity at start of cycle
    capacitySpare = self.capacity - self.amc
    vwc = int((self.amc / self.capacity) * 100 )
    vwcGroup = int(vwc/vwcIncrement) * vwcIncrement
    vwcRow =  int(vwc/vwcIncrement)
    print(' ')
    print('INITIAL CAPACITY')
    print('capacitySpare ', capacitySpare , ' = self.capacity ', self.capacity, ' - self.amc', self.amc)
    print('vwcGroup (5,10,15,...,100): ', vwcGroup, ' from ', vwc)
    print('vwcRow:(0-19) ', vwcRow)

    # rain, uncontrolled cannot be negative numbers
    self.rain = rainIntensity * self.duration
    self.uncontrolled = uncontrolled * self.duration
    print(' ')
    print('UNCONTROLLED INPUTS')

    print('rain', self.rain)
    print('rainIntensity', rainIntensity)
    
    intensityColumn = int(rainIntensity/rainIntensityIncrement)
    if intensityColumn > rainIntensityIncrements - 1:
      intensityColumn = rainIntensityIncrements - 1
    print('intensityColumn', intensityColumn)
    print('uncontrolled', self.uncontrolled)

    efficiency = self.product['efficiency'][vwcRow][intensityColumn]
    print(' ')
    print('EFFICIENCY')
    print('efficiency: ',efficiency)

    # calculate controlled inputs, factor in weather later
    if self.rain > 0 or uncontrolled > 0: # no controlled release during rain
      self.controlled = 0
    elif (vwc < self.controlledLo) or (vwc > self.controlledHi): # no controlled release outside vwc parameters
      self.controlled = 0
    elif (self.controlledRate * self.duration) > capacitySpare: # no controlled release if it would put us over capacity
      self.controlled = 0
    else:
      self.controlled = self.controlledRate * self.duration
    print(' ')
    print('CONTROLLED INPUTS')
    print('controlled', self.controlled)

    self.input = self.rain + self.uncontrolled + self.controlled
    print(' ')
    print('TOTAL INPUTS')
    print('input', self.input)

    if self.input <= capacitySpare:
      self.absorb = self.input * efficiency/100
    # if input > capacity, absorb to capacity, rest runs off (add eff. factor later)
    else:
      self.absorb = 0

    self.runoff = self.input - self.absorb
    retPre = self.amc + self.absorb
    print(' ')
    print('RETENTION & RUNOFF')
    print('absorbtion' , self.absorb)
    print('preliminary retention' , retPre)
    print('runoff ', self.runoff, ' to ', self.runoffTo)
    
    hourColumn = int( (self.minutes %  self.minsDay) / self.minsEtSlot ) # calc which 2-hour column we are in
    monthRow = 6 # get from effective date
    etRate = self.etTable['table'][monthRow][hourColumn] # gal/sf/min
    etMax = etRate * duration # gal/sf/min
    # no ET during rain
    if self.rain > 0:
      self.et = 0
    elif etMax > retPre:
      self.et = retPre  # ET cannot exceed retention... improve this... as vwc drops, et is more difficult to extract
    else:
      self.et = etMax
    print(' ')
    print('LOSSES')
    print('effective date') # calculate this
    print('hourColumn', hourColumn)
    print('monthRow', monthRow)
    print('etRate', etRate)
    print('etMax', etMax)
    print('ET', self.et)

    self.ret = retPre - self.et
    self.amc = self.ret
    print(' ')
    print('FINAL')
    print('retention post ET', self.ret)
    print('amc for next cycle', self.amc)

    self.minutes += duration
    self.month = int(self.minutes/self.minsMonth)+1
    print(' ')
    print('INCREMENT')
    print('minutes for next cycle ', self.minutes)
    print('month for next cycle ', self.month)

# create a loop
# accumulate total rain
# create Cistern class to use for controlled release, accumulate release (can get into negative numbers for now)
# create Offsite class to contain runoff, accumulate runoff

duration =                data['general']['vwcIncrement']
rainIntensityIncrement =  data['general']['rainIntensityIncrement']
rainIntensityIncrements = data['general']['rainIntensityIncrements']
vwcIncrement =            data['general']['vwcIncrement']
surface =                 "two"


print('duration', duration)
print('rainIntensityIncrement', rainIntensityIncrement)
print('vwcIncrement', vwcIncrement)
print('surface', surface)

surface1 = Surface(duration,rainIntensityIncrement,rainIntensityIncrements,vwcIncrement,surface)

rainTable = data['events']['rainIntensity']

for event in rainTable:
  surface1.cycle(event,0)


# surface1.cycle(5,0.3,0)
# surface1.cycle(5,0.3,0)
# surface1.cycle(5,0.3,0)
# surface1.cycle(50,0,0)
# surface1.cycle(5,0,0)
# surface1.cycle(15,0.1,0)
# surface1.cycle(5,0,0)
# surface1.cycle(35,0,0)
# surface1.cycle(10,0,0)
# surface1.cycle(10,0,0)
# surface1.cycle(10,0,0)
