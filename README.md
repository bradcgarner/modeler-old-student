# stormwater-modeler

modeler.py

class Event
initializes with event data, from Surface

class Surface
  initializes with data from surface, as input from user
  cycle generates the model
    calculate
      capacity at start of cycle
      uncontrolled inputs (rain, uncontrolled inflow)
      controlled inputs
      efficiency of absorption (using product data)
      inputs: actual absorption [absorb inputs]
      output: runoff
      output: et
      finalize retention: input less output
    save output for 1 cycle (write to csv and/or db)
    calculate events
      event calcs are an O(n) algorithm that look for a gap in rain of X duration
      events start when it rains
      each event has 2 phases: wet and dry (raining and not raining)
      if there is any gap in rain, a marker indicates the start of gap
      if it rains before the status has changed to dry, the marker moves
      if the gap grows to X duration, the event status changes from wet to dry, starting at the marker
      after a status is dry (which is only set after X duration), upon rain, the event # increments
    save output for event (to be written at end to csv and/or db)
    increment the cycle
      e.g. if we model 48 hours at 5 minute intervals, that's 576 cycles; we run each surface for cycle 1, then each surface for #2, etc.
  calculate volume of runoff received from other surfaces
  
      
