import math

class Physics:

  ENCmomentaryCurrentConsumption = 0.0
  ENCbatteryValue = 0.0

  NNSxVal = 0
  NNSyVal = 0
  NNSspeed = 0.0
  NNSmaxSpeed = 0.0
  NNSheading = 0.0 #radians - value from 0 to 2pi

  loaded = False
  directionFront = True

  def __init__(self,currentConsumption, battery): # argument agv
    self.ENCmomentaryCurrentConsumption = currentConsumption
    self.ENCbatteryValue = battery
  
  def emergencyStop(self):
    self.NNSspeed = 0
    self.drainBattery(1)
    
  def rotate(self,rad):
    self.NNSheading = rad
    self.drainBattery(.1)
  
  def accelerate(self):
    if self.NNSspeed < self.NNSmaxSpeed:
      self.NNSspeed += 0.1
      self.drainBattery(.2)
  
  def updatePosition(self):
    self.NNSxVal += math.cos(self.radiansToDegrees(self.NNSheading))*self.NNSspeed
    self.NNSyVal += math.sin(self.radiansToDegrees(self.NNSheading))*self.NNSspeed
    self.drainBattery(.1)

  def drainBattery(self, val):
    self.ENCbatteryValue -= val

  def update(self):
    self.updatePosition
    self.drainBattery(.1)

  def radiansToDegrees(val):
    return val*180/math.pi


    
