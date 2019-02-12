import time
import json

from BME280 import BME280
from temp_repo import TemperatureRepository

with open('db_config.json') as inf:
  dbconfig = json.load(inf)

repo = TemperatureRepository(**dbconfig)

temp_reader = BME280()

while True:
  temp = temp_reader.read()
  repo.insert_temp(temp)
  time.sleep(300)
