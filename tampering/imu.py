import time
import board
import adafruit_bno055


i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
sensor.mode = adafruit_bno055.MAGGYRO_MODE


def temperature():
    result = sensor.temperature
    if result <= 0:
        result = 128 + result
    else:
        pass
    return result

while True:
    print("Temperature: {} degrees C".format(temperature()))
    #print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    #print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    #print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print("Calibration {} done".format(sensor.calibration_status))
    print("Euler angle: {}".format(sensor.euler))
    #print("Quaternion: {}".format(sensor.quaternion))
    #print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    #print("Gravity (m/s^2): {}".format(sensor.gravity))
    print()
    time.sleep(3)

"""
Att göra för IMUn: Få systemet kalibrerat genom att ta initalvärdena från en första läsning och sedan kunna kalla på dessa från en extern EEEPROM (antagligen raspberry pi:n).

Sedan ska vi få hela projektet att fungera så vi kan testa olika IMU-setups för att avgöra om någon tamperat med brandsläckaren, kan man t.ex. utgå enbart från gyroskopet så att
man kan minimera konstruktionen on-chip för senare?

Till sist ska även en enkel magnetlist undersökas och se om det räcker för att undersöka så att brandsläckaren ej har tameprats med.

Bra info finns på sidan: https://www.allaboutcircuits.com/projects/bosch-absolute-orientation-sensor-bno055/
"""