import time
import json

from BME280 import BME280
from TSL2561 import TSL2561
from temp_repo import TemperatureRepository

with open('db_config.json') as inf:
  dbconfig = json.load(inf)

repo = TemperatureRepository(**dbconfig)

temp_reader = BME280()
lux_reader = TSL2561()

while True:
  temp = temp_reader.read()
  repo.insert_temp(temp)
  lux = lux_reader.read()
  repo.insert_lux(lux)
  time.sleep(300)
