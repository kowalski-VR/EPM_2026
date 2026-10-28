#!/usr/bin/env pybricks-micropython


# Hier werden die erforderlichen Software-Module importiert. Dabei sollte nichts verändert werden
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, GyroSensor, UltrasonicSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

# Import der eigenen Funktionen
from funktionen import *

# Hardware einrichten
ev3 = EV3Brick()
tastsensor = TouchSensor(Port.S4)
abstandssensor = UltrasonicSensor(Port.S2)
gyro_sensor  = GyroSensor(Port.S3)
farbsensor = ColorSensor(Port.S1)
motorR = Motor(Port.B)
motorL = Motor(Port.C)
motorFlagge = Motor(Port.D)



# Globale Variablen
geschwindigkeit = 500   # "Mastergeschwindigkeit" - alle nötigen Größen skalieren mit ihr



# ======================   
# Main
# ======================
def main(): 
    """Hauptfunktion
    """
    # Ready Check - Roboter ist bereit
    ev3.speaker.beep()

    # Startvorgang
    while not tastsensor.pressed():
        pass
    while tastsensor.pressed():
        pass
    ev3.speaker.beep()

    wait(500)

    drehen_gyro_reglerbasiert(motorL, motorR, gyro_sensor, 180, -1)
    wait(100)

    labyrinth(geschwindigkeit, motorL, motorR, motorFlagge, abstandssensor, tastsensor, gyro_sensor, farbsensor)

    # while (not tastsensor.pressed()) and (abstandssensor.distance() < 300):
    #     fahren_wand(geschwindigkeit, motorL, motorR, abstandssensor)
    #     wait(10)
    # stop(motorL, motorR)

    # fahren_gerade(geschwindigkeit, motorL, motorR)
    # wait(200)
    # stop(motorL, motorR)

    # drehen_gyro_reglerbasiert(motorL, motorR, gyro_sensor, 180, 1)
    # wait(1000)
    # drehen_gyro_reglerbasiert(motorL, motorR, gyro_sensor, 180, 1)
    
    
    # Signal - Ziel erreicht
    for i in range(5):
        ev3.speaker.beep(i*100)
        time.sleep_ms(125)
    
if __name__ == '__main__':
    main()
