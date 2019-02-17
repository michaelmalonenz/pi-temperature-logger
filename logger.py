import time
import json

from gpiozero import Button, RGBLED, Device
from BME280 import BME280
from TSL2561 import TSL2561
from ssd1306 import SSD1306
from temp_repo import TemperatureRepository

lcd = SSD1306(spi_bus=0, spi_device=0, pin_dc=23, pin_reset=24)
lcd.hardware(remap_segment=True, alternative_com_pin=True, remap_scan_direction=True)

lcd.contrast(40)
lcd.paint()
lcd.on()

# Light all the corners
lcd.xy(0, 0, 1)
lcd.xy(0, 63, 1)
lcd.xy(127, 0, 1)
lcd.xy(127, 63, 1)
lcd.paint()

# Write some text
lcd.text(28, 28, "Hello world!", size=1)
lcd.paint()

led = RGBLED(red=22, green=20, blue=21)
button = Button(4)

def button_press():
  temp = temp_reader.read()
  colour = (0, 0, 0)
  if temp.temperature > 30:
    colour = (1, 0, 0) # red
  elif temp.temperature > 25:
    colour = (1, 0.5, 0) # orange
  elif temp.temperature > 20:
    colour = (1, 1, 0) # yellow
  elif temp.temperature > 15:
    colour = (0.5, 1, 0) # lime
  elif temp.temperature > 10:
    colour = (0, 1, 0) # green
  elif temp.temperature > 5:
    colour = (0, 1, 0.5) # cyan
  else:
    colour = (0, 0, 1) # blue
  led.color = colour

def release():
  led.off()


with open('db_config.json') as inf:
  dbconfig = json.load(inf)

repo = TemperatureRepository(**dbconfig)

temp_reader = BME280()
lux_reader = TSL2561()
button.when_pressed = button_press
button.when_released = release

try:
  while True:
    temp = temp_reader.read()
    repo.insert_temp(temp)
    lux = lux_reader.read()
    repo.insert_lux(lux)
    button.wait_for_press(300)
except KeyboardInterrupt:
  button.close()
  led.close()
  lcd.reset()
