import time
import atexit
import pigpio

class sensor:
   def __init__(self, pi, gpio, LED=None, power=None):
      self.pi = pi
      self.gpio = gpio
      self.LED = LED
      self.power = power

      if power is not None:
         pi.write(power, 1)
         time.sleep(2)

      self.powered = True

      self.cb = None

      atexit.register(self.cancel)

      self.bad_CS = 0
      self.bad_SM = 0
      self.bad_MM = 0
      self.bad_SR = 0

      self.no_response = 0
      self.MAX_NO_RESPONSE = 2

      self.rhum = -999
      self.temp = -999

      self.tov = None

      self.high_tick = 0
      self.bit = 40

      pi.set_pull_up_down(gpio, pigpio.PUD_OFF)

      pi.set_watchdog(gpio, 0)

      self.cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cb)

   def _cb(self, gpio, level, tick):
      diff = pigpio.tickDiff(self.high_tick, tick)

      if level == 0:
         if diff >= 50:
            val = 1
            if diff >= 200:
               self.CS = 256
         else:
            val = 0

         if self.bit >= 40:
            self.bit = 40

         elif self.bit >= 32:
            self.CS  = (self.CS<<1)  + val

            if self.bit == 39:
               self.pi.set_watchdog(self.gpio, 0)

               self.no_response = 0

               total = self.hH + self.hL + self.tH + self.tL

               if (total & 255) == self.CS:

                  self.rhum = ((self.hH<<8) + self.hL) * 0.1

                  if self.tH & 128:
                     mult = -0.1
                     self.tH = self.tH & 127
                  else:
                     mult = 0.1

                  self.temp = ((self.tH<<8) + self.tL) * mult

                  self.tov = time.time()

                  if self.LED is not None:
                     self.pi.write(self.LED, 0)

               else:

                  self.bad_CS += 1

         elif self.bit >=24:
            self.tL = (self.tL<<1) + val

         elif self.bit >=16:
            self.tH = (self.tH<<1) + val

         elif self.bit >= 8:
            self.hL = (self.hL<<1) + val

         elif self.bit >= 0:
            self.hH = (self.hH<<1) + val

         else:
            pass

         self.bit += 1

      elif level == 1:
         self.high_tick = tick
         if diff > 250000:
            self.bit = -2
            self.hH = 0
            self.hL = 0
            self.tH = 0
            self.tL = 0
            self.CS = 0

      else:
         self.pi.set_watchdog(self.gpio, 0)
         if self.bit < 8:
            self.bad_MM += 1
            self.no_response += 1
            if self.no_response > self.MAX_NO_RESPONSE:
               self.no_response = 0
               self.bad_SR += 1
               if self.power is not None:
                  self.powered = False
                  self.pi.write(self.power, 0)
                  time.sleep(2)
                  self.pi.write(self.power, 1)
                  time.sleep(2)
                  self.powered = True
         elif self.bit < 39:
            self.bad_SM += 1
            self.no_response = 0

         else:
            self.no_response = 0

   def temperature(self):
      return self.temp

   def humidity(self):
      return self.rhum

   def staleness(self):
      if self.tov is not None:
         return time.time() - self.tov
      else:
         return -999

   def bad_checksum(self):
      return self.bad_CS

   def short_message(self):
      return self.bad_SM

   def missing_message(self):
      return self.bad_MM

   def sensor_resets(self):
      return self.bad_SR

   def trigger(self):
      if self.powered:
         if self.LED is not None:
            self.pi.write(self.LED, 1)

         self.pi.write(self.gpio, pigpio.LOW)
         time.sleep(0.017) # 17 ms
         self.pi.set_mode(self.gpio, pigpio.INPUT)
         self.pi.set_watchdog(self.gpio, 200)

   def cancel(self):

      self.pi.set_watchdog(self.gpio, 0)

      if self.cb != None:
         self.cb.cancel()
         self.cb = None

if __name__ == "__main__":
   import time
   import pigpio
   import DHT22

   INTERVAL=3
   pi = pigpio.pi()
   s = DHT22.sensor(pi, 22)
   r = 0
   next_reading = time.time()
   while True:
      r += 1
      s.trigger()
      time.sleep(0.2)

      print("{} {} {} {:3.2f} {} {} {} {}".format(
         r, s.humidity(), s.temperature(), s.staleness(),
         s.bad_checksum(), s.short_message(), s.missing_message(),
         s.sensor_resets()))
      g = s.humidity()
    
      next_reading += INTERVAL
      time.sleep(next_reading-time.time())

   s.cancel()
   pi.stop()

