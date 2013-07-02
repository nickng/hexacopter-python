"""Defines public functions and classes not part of the CMSIS driver library.
"""

from internals import robocaller, cstruct, malloc, free, isr_list

__author__ =      "Neil MacMunn"
__email__ =        "neil@gumstix.com"
__copyright__ =   "Copyright 2010, Gumstix Inc."
__license__ =     "BSD 2-Clause"
__version__ =      "0.1"

class Array(object):
  """Allocates and initializes an array in RoboVero RAM.
  """
  def __init__(self, length, size, values=[]):
    self.length = length
    self.size = size
    self.ptr = malloc(size * length)
    
    # assign the same value to all items
    if type(values) == int:
      for i in range(length):
        self[i] = values
    
    # copy a list of values
    elif type(values) == list:
      for i in range(min(length, len(values))):
        self[i] = values[i]
        
    # convert a string to a list of characters and copy
    elif type(values) == str:
      values = list(values)
      for i in range(min(length, len(values))):
        self[i] = ord(values[i])

  def __getitem__(self, key):
    if key >= self.length:
      raise IndexError
    return robocaller("deref", "int", self.ptr + self.size*key, self.size)

  def __setitem__(self, key, value):
    if key >= self.length:
      raise IndexError
    if type(value) != int:
      raise TypeError
    robocaller("deref", "void", self.ptr + self.size*key, self.size, value)
    
  def __del__(self):
    free(self.ptr)

def roboveroConfig():
  """Configure the microcontroller pin select registers according to the labels
  on the RoboVero board.
  """
  return robocaller("roboveroConfig", "void")
  
def heartbeatOn():
  """Flash the onboard LED.
  """
  return robocaller("heartbeatOn", "void")
  
def heartbeatOff():
  """Let user control the onboard LED.
  """
  return robocaller("heartbeatOff", "void")

def initMatch(ch, count):
  """Initialize a PWM match condition.
  """
  return robocaller("initMatch", "void", ch, count)
  
def registerCallback(IRQn, function):
  """Register a RoboVero interrupt service routine.
  
  Pass the IRQ number and function to call when an interrupt occurs.
  """
  isr_list[IRQn] = function

def PWM_SetSpeed(PWMChannel, PWMPeriod, PWMBasePeriod):
    """This function sets the PWM channel to output specified PWM wave

   Note:
    - All channels must use same base period since they share
   PWM0's counter as base period.
   - You can set all six pwm channels to output different duty cycles.

   Example: to output wave of 2000us period and set 1500us of the
   period to logic one to hold a neutral position for angle servo
   for channel 2.

    PWMChannel: 1-6, the PWM channel number.
    PWMPeriod:  the time for the chnnel to output logic one in each cycle, in us.
    PWMBasePeriod: the period of each cycle, in us.
    """
    return robocaller("PWM_SetSpeed", "void", PWMChannel, PWMPeriod, PWMBasePeriod)

def PWM_CounterState(PWMChannel, NewState):
    return robocaller("PWM_CounterState", "void", PWMChannel, NewState)
