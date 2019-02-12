from db_accessor import DatabaseAccessor

class TemperatureRepository(DatabaseAccessor):

  def insert_temp(self, temp):
    sql = """
    INSERT INTO temperatures (temperature, pressure, humidity, time)
    VALUES (%(temperature)s,%(pressure)s,%(humidity)s, NOW());
    """
    params = {
      'temperature': temp.temperature,
      'pressure': temp.pressure,
      'humidity': temp.humidity,
    }
    self.execute(sql, params)
