import sqlite3
import gpiozero
import datetime as time
from time import sleep
import Adafruit_DHT as sensor_dht11

# Der bliver oprettet variabler til sensoren
sensor_type = sensor_dht11.DHT11
sensor_pin = 17

# SQLite database oprettes
database_connection = sqlite3.connect('dht11_sensor_data.db')
database_cursor = database_connection.cursor()

# SQLite-databasen opretter tabellen Measurements med kolonnerne temperatur, luftfugtighed og tidspunkt.
database_cursor.execute('CREATE TABLE IF NOT EXISTS Measurements(Temperature REAL, Humidity REAL, Time TEXT)')
database_connection.commit()

# Sensor indsamler data
def read_sensor_data():
    temperature, humidity = sensor_dht11.read_retry(sensor_type, sensor_pin)
    return temperature, humidity

# Indsættelse af målinger i databasen
def insert_measurement_into_database(temperature, humidity):
    current_timestamp = time.time.now().strftime("%Y-%m-%d %H:%M:%S")
    measurement_data = (temperature, humidity, current_timestamp)
    insert_query = "INSERT INTO Measurements (Temperature, Humidity, Time) VALUES (?, ?, ?)"
    database_cursor.execute(insert_query, measurement_data)
    database_connection.commit()

# Løkke som opdaterer databasen hvert 10 sekund
while True:
    temperature, humidity = read_sensor_data()
    if humidity is not None and temperature is not None:
        insert_measurement_into_database(temperature, humidity)
    sleep(10)

database_connection.close()
