# stormwater-modeler

modeler.py

continual vs categorical variables


input: project
  project has a list of rain events (list of numbers, each list item represents a cycle, each number represents a volume of rain during that cycle)
  project has a list of surfaces
  run a cycle for each surface for event on the list (will likely be hundreds, or tens of thousands of cycles)
    E.g. surface a, cycle 1; surface b, cycle 1; surface a, cycle 2; surface b, cycle 2; etc.
  each cycle:
    collects runoff 
      empty list is created at start of cycle
      1st surface populates runoff
      2nd surface receives runoff from 1st (if set to receive from #1)
      2nd surface populates runoff
      3rd surface receives, etc.
    calculates:
      capacity at start of cycle
      uncontrolled inputs (rain, uncontrolled inflow)
      controlled inputs
      efficiency of absorption (using product data)
      inputs: actual absorption [absorb inputs]
      output: runoff
      output: et
      finalize retention: input less output
    saves output for 1 cycle (write to csv and/or db)
    calculatess events
      event calcs are an O(n) algorithm that look for a gap in rain of X duration
      events start when it rains
      each event has 2 phases: wet and dry (raining and not raining)
      if there is any gap in rain, a marker indicates the start of gap
      if it rains before the status has changed to dry, the marker moves
      if the gap grows to X duration, the event status changes from wet to dry, starting at the marker
      after a status is dry (which is only set after X duration), upon rain, the event # increments
    saves output for event (to be written at end to csv and/or db)
    increments the cycle
     
  calculate volume of runoff received from other surfaces
  
      

   
class Event
initializes with event data, from Surface

class Surface
  initializes with data from surface, as input from user
  cycle generates the model
    
