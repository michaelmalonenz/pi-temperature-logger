from db_accessor import DatabaseAccessor

class TemperatureRepository(DatabaseAccessor):

  def insert_temp(self, temp):
    sql = """
    INSERT INTO temperatures (temperature, pressure, humidity, timestamp)
    VALUES (%(temperature)s,%(pressure)s,%(humidity)s, NOW());
    """
    params = {
      'temperature': temp.temperature,
      'pressure': temp.pressure,
      'humidity': temp.humidity,
    }
    self.execute(sql, params)

  def insert_lux(self, lux):
    sql = """
    INSERT INTO lux (infrared, visible, timestamp)
    VALUES (%(infrared)s,%(visible)s,NOW());
    """
    params = {
      'infrared': lux.infrared,
      'visible': lux.visible
    }
    self.execute(sql, params)
