import json
import math
# that is like require(express)

with open('inputs.json') as f:
  data = json.load(f)



class Surface:
  def __init__(self, duration,rainIntensityIncrement,vwcIncrement,product,capacity):
    self.amc = 0  # antecedent moisture condition g/sf
    self.duration = duration # minutes
    self.rainIntensityIncrement = rainIntensityIncrement # g/sf/min
    self.vwcIncrement = vwcIncrement # integer 0-100 (usually 5)

    self.controlledLo = 0      # vwc (integer 0-100)
    self.controlledHi = 70     # vwc (integer 0-100)
    self.controlledRate = 0.05 # g/sf/min
    
    self.product = product     # index of product in array
    self.capacity = capacity   # g/sf


  print('duration = 5: ',self.duration)
  print('capacity g/sf = 0.50 ',self.capacity)
  print('rainRateIncrement = 0.0007 ',rainIntensityIncrement)
  print('vwcIncrement = 5: ',self.vwcIncrement)

  def cycle(self, rain, uncontrolled):
    # rain, uncontrolled are volume in gals/sf/minute

    # calculate capacity at start of cycle
    capacitySpare = self.capacity - self.amc
    vwc = math.floor((self.amc / self.capacity) * 100 )
    vwcGroup = math.floor(vwc/vwcIncrement) * vwcIncrement
    vwcSlot =  math.floor(vwc/vwcIncrement)
    efficiencySlot = math.floor(0.0015/rainRateIncrement) -1
    efficiency = data['system'][product]['efficiency'][vwcSlot][efficiencySlot]
    print(' ')
    print('INITIAL CAPACITY')
    print('capacitySpare ', capacitySpare , ' = self.capacity ', self.capacity, ' - self.amc', self.amc)
    print('vwcGroup: ', vwcGroup, ' from ', vwc)
    print('vwcSlot: ',vwcSlot)
    print('efficiencySlot = 1: ',efficiencySlot)
    print('efficiency: ',efficiency)

    # rain, uncontrolled cannot be negative numbers
    self.rain = rain * self.duration
    self.uncontrolled = uncontrolled * self.duration
    print(' ')
    print('UNCONTROLLED INPUTS')
    print('rain', self.rain)
    print('uncontrolled', self.uncontrolled)

    # calculate controlled inputs, factor in weather later
    if self.rain > 0 or uncontrolled > 0:
      self.controlled = 0
    elif vwc < self.controlledLo or vwc > self.controlledHi
      self.controlled = 0
    elif (self.controlledRate * self.duration) > self.capacitySpare
      self.controlled = 0
    else:
      self.controlled = self.controlledRate * self.duration
    print(' ')
    print('CONTROLLED INPUTS')
    print('controlled', self.controlled)

    self.input = self.rain + self.uncontrolled + self.controlled
    # if input <= capacity, absorb it all (add efficiency factor later)
    if self.input <= capacitySpare:
      self.absorb = self.input
      self.runoff = 0 
    # if input > capacity, absorb to capacity, rest runs off (add eff. factor later)
    else:
      self.absorb = self.capacitySpare
      self.runoff = self.input - self.capacitySpare


    print('surfaces 2 runoff = 3: ',data['surfaces'][i]['runoff'])
    
    retPre = self.amc + self.absorb
    # et needs to refer to a lookup table
    etRaw = 0.05 * duration
    # no ET during rain
    if self.rain > 0:
      self.et = 0
    # ET cannot exceed retention
    elif etRaw > retPre:
      self.et = retPre
    else:
      self.et = etRaw
    self.ret = retPre - self.et
    print(' ')
    print('total input', self.input)
    print('   controlled', self.controlled)
    print('      raw controlled', controlledRaw)
    print('absorb', self.absorb)
    print('runoff', self.runoff)
    print('ret pre ET', retPre)
    print('raw ET', etRaw)
    print('ET', self.et)
    print('ret post ET', self.ret)
    self.amc = self.ret

# create a loop
# accumulate total rain
# create Cistern class to use for controlled release, accumulate release (can get into negative numbers for now)
# create Offsite class to contain runoff, accumulate runoff

duration =               data['general']['vwcIncrement']
rainIntensityIncrement = data['general']['rainRateIncrement']
vwcIncrement =           data['general']['vwcIncrement']

product =                0
capacity =               data['system']['capacityGsf']

surface1 = Surface(duration,rainIntensityIncrement,vwcIncrement,product,capacity)

surface1.cycle(5,0.3,0)
surface1.cycle(5,0.3,0)
surface1.cycle(5,0.3,0)
surface1.cycle(5,0.3,0)
surface1.cycle(50,0,0)
surface1.cycle(5,0,0)
surface1.cycle(15,0.1,0)
surface1.cycle(5,0,0)
surface1.cycle(35,0,0)
surface1.cycle(10,0,0)
surface1.cycle(10,0,0)
surface1.cycle(10,0,0)
