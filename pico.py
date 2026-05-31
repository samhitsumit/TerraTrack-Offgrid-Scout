from machine import Pin, UART, I2C
from time import sleep, time, time_ns, localtime
import lcd_api
import i2c_lcd
import bme280
import network
import socket

log_button = Pin(16, Pin.IN, Pin.PULL_UP)
global gps_serial
gps_serial = True

lcd_state = True
GeoJsonDict = None

def writeToLogsFolder(data):
    fn = f"{localtime()[2]}{localtime()[1]}{localtime()[0]}_{localtime()[3]}{localtime()[4]}{localtime()[5]}.json"
    with open(f"location logs/{fn}", "w") as file:
        file.write(str(data))

def formatRawJson(lati, loni, humid, tempe):
    return [
        {"datetime": {
            "Day":   localtime()[2],
            "Month": localtime()[1],
            "Year":  localtime()[0],
            "Hour":  localtime()[3],
            "Minute":localtime()[4],
            "Second":localtime()[5],
            "utime": time_ns()
        },
         "Sensor data": {
            "lat": lati,
            "lon": loni,
            "humid": humid / 1024,
            "temp": tempe / 100
         }
        }
    ]

def formatGeoJsonDict(lati, longi, temp, hume):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [longi, lati]
        },
        "properties": {
            "name": "Googleplex",
            "notes": f"Temperature: {temp}, Humidity: {hume}"
        }
    }

old_lat = old_lon = None
button = Pin(17, Pin.IN, Pin.PULL_UP)
# Setup UART for GPS
gps_serial = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# Setup I2C for BME280
bmeI2C = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
sensor = bme280.BME280(i2c=bmeI2C)

# Optional: another I2C for LCD (currently commented out)
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
lcd = i2c_lcd.I2cLcd(i2c, 0x27, 4, 20)
lcd.clear()

# print("BME I2C address:", bmeI2C.scan())

latitude = longitude = 0.0
buffer = ""

def convert_to_decimal(coord, direction):
    if not coord:
        return None
    degrees = int(coord[:2] if direction in ['N', 'S'] else coord[:3])
    minutes = float(coord[2:] if direction in ['N', 'S'] else coord[3:])
    decimal = degrees + (minutes / 60)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def parse_gprmc(line):
    global old_lat, old_lon, latitude, longitude
    parts = line.split(',')
    if parts[0] == '$GPRMC' and parts[2] == 'A':  # Valid fix
        raw_lat = parts[3]
        lat_dir = parts[4]
        raw_lon = parts[5]
        lon_dir = parts[6]

        latitude = convert_to_decimal(raw_lat, lat_dir)
        longitude = convert_to_decimal(raw_lon, lon_dir)

        print("Latitude: {:.6f}".format(latitude))
        print("Longitude: {:.6f}".format(longitude))
    else:
        print("No valid GPS fix.")

# -------------------------
#        MAIN LOOP
# -------------------------
while True:
    try:
        print(button.value())  
        if button.value() == 1:
            lcd_state = False
            
        else:
            lcd_state = True
            
        print(lcd_state)
            
          

        # Always read and print temperature/humidity
        temp, pressure, humidity = sensor.read_compensated_data()
        print("Temperature: {:.2f} °C".format(temp))
        print("Pressure: {:.2f} hPa".format(pressure / 100))  # Convert Pa → hPa
        print("Humidity: {:.2f} %".format(humidity))

        # Uncomment if using LCD
        
        if lcd_state:
            print("Hi im running")
            lcd.backlight_on()
            lcd.display_on()
            lcd.move_to(0, 2)
            lcd.putstr("Temp:      {:5.1f} ".format(temp))
            lcd.move_to(0, 3)
            lcd.putstr("Humidity:  {:5.1f} %".format(humidity))
            
        else:
            lcd.backlight_off()
            lcd.clear()
            lcd.display_off()
        

        # Handle GPS data if available
        if gps_serial.any():
            data = gps_serial.read(gps_serial.any())
            try:
                buffer += data.decode('utf-8')
            except UnicodeError:
                print("Failed to parse. Skipping line")

            lines = buffer.split('\n')
            for line in lines[:-1]:
                line = line.strip()
                if line.startswith('$'):
                    parse_gprmc(line)
            buffer = lines[-1]
            
        print(log_button.value())  
        # Handle log button
        if log_button.value() == 0:
            
            lcd.clear()
            lcd.putstr("Saving...")
            
            data = formatRawJson(latitude, longitude, humidity, temp)
            writeToLogsFolder(data)
            while log_button.value() == 0:
                print(log_button.value())
                sleep(0.05)

        sleep(1)

    except Exception as e:
        print("Error:", e)
        sleep(1)
