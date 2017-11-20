import json
# that is like require(express)

with open('inputs.json') as f:
  data = json.load(f)

print(data['increments'])

class Surface:
  def __init__(self, ret):
    self.amc = ret

  # variables below should read from another class 'covering'
  slope = 0.25
  cover = 'green roof'
  capacityTot = 4

  def perform(self, duration, rain, uncontrolled):
    # duration is minutes, 3 other args are volume in gals/minute
    self.capacitySpare = self.capacityTot - self.amc
    # duration, rain, uncontrolled, controlled cannot be negative numbers
    self.duration = duration
    self.rain = rain * duration
    self.uncontrolled = uncontrolled * duration
    # controlled needs a lookup table, factor in % of capacity, weather
    controlledRaw = .05 * duration
    if self.rain > 0 or uncontrolled > 0:
      self.controlled = 0
    elif controlledRaw > self.capacitySpare:
      self.controlled = self.capacitySpare
    else:
      self.controlled = controlledRaw
    self.input = self.rain + self.uncontrolled + self.controlled
    # if input <= capacity, absorb it all (add efficiency factor later)
    if self.input <= self.capacitySpare:
      self.absorb = self.input
      self.runoff = 0 
    # if input > capacity, absorb to capacity, rest runs off (add eff. factor later)
    else:
      self.absorb = self.capacitySpare
      self.runoff = self.input - self.capacitySpare
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
    print('amc', self.amc)
    print('spare capacity', self.capacitySpare)
    print('total input', self.input)
    print('   rain', self.rain)
    print('   uncontrolled', self.uncontrolled)
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
surface1 = Surface(0.5)

surface1.perform(5,0.3,0)

surface1.perform(5,0.3,0)

surface1.perform(5,0.3,0)

surface1.perform(5,0.3,0)

surface1.perform(50,0,0)

surface1.perform(5,0,0)

surface1.perform(15,0.1,0)

surface1.perform(5,0,0)

surface1.perform(35,0,0)

surface1.perform(10,0,0)

surface1.perform(10,0,0)

surface1.perform(10,0,0)
