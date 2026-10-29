# Hier werden die erforderlichen Software-Module importiert.
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, GyroSensor, UltrasonicSensor)
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.parameters import Port, Stop, Direction, Button, Color
import time
import math

# ein Feld = 30 cm

# ==================
# Fahren (geradeaus)
# ==================
# für alternative Ansätze: README Abschnitt 5.4 Gerades Fahren
def fahren_gerade(geschwindigkeit: int, motorL:Motor, motorR:Motor):
    """ Drehen der Motoren mit einer konstanten Geschwindigkeit.

    Args:
            motorL (Motor): Linker Motor
            motorR (Motor): Rechter Motor
    """
    motorL.run(geschwindigkeit)
    motorR.run(geschwindigkeit)



# ==========================================================================
# Stoppen der Motoren
# ==========================================================================
# für alternative Ansätze: README Abschnitt 5.4 Gerades Fahren
def stop(motorL:Motor, motorR:Motor):
    """ Stoppen der Motoren mittels der Hold-Funktion.
        .hold stoppt die Motoren sofort und hält diese in ihrer aktuellen Position fest.

    Args:
        motorL (Motor): Linker Motor
        motorR (Motor): Rechter Motor
    """
    motorL.hold()
    motorR.hold()



# ============================================================
# Drehen des Roboters mittels des Gyrosensors und einem Regler
# ============================================================
# für alternative Ansätze: README Abschnitt 5.5 Drehen
def drehen_gyro_reglerbasiert(motorL:Motor, motorR:Motor, gyro_sensor:GyroSensor, drehwinkel:int, drehrichtung:int):
    """ Eine Methode zum Drehen des Roboters. 
        Nutzt den Gyrosensor und einen Regler zum gradiellen Anfahren und Abbremsen

    Args:
        motorL (Motor): Linker Motor
        motorR (Motor): Rechter Motor
        gyro_sensor (GyroSensor): Gyroskopischer Sensor
        drehwinkel (int): Absoluter Winkel in Grad, um den sich der Roboter drehen soll
        drehrichtung (int): Drehrichtung -> (+1) im Uhrzeigersinn, (-1) gegen den Uhrzeigersinn
    """
    # Maximalgeschwindigkeit
    v_max = 450 # [Grad/s]
    # Verstärkungsfaktor des P-Reglers
    Kp = 3 * (v_max/400) # [1/s]
    # Mindestgeschwindigkeit
    v_min = 90 # [Grad/s]
    # Maximale Geschwindigkeitsänderung pro Schleifendurchlauf / Gradientenbegrenzung
    v_diff_max = 10 # [Grad/s]
    # Zulässige Winkelabweichung
    toleranz = 2 # [Grad]
    # Geschwindigkeit des vorherigen Schleifendurchlaufs
    v_vor = 0 # [Grad/s]

    # Auslesen des aktuellen Drehwinkels durch den Gyro-Sensor
    startwinkel = gyro_sensor.angle() # [Grad]
    # Berechnen des Sollwinkels
    zielwinkel = startwinkel + drehrichtung * drehwinkel # [Grad]

    # Drehen bis der Toleranzbereich erreicht wurde
    while (((zielwinkel - gyro_sensor.angle()) * drehrichtung) > toleranz):
        # Berechnen der aktuellen Winkelabweichung
        abweichung = abs(zielwinkel - gyro_sensor.angle())

        # Berechnen der Sollgeschwindigkeit mit dem P-Regler und der Gradientenbegrenzung
        geschwindigkeit = min(v_vor + v_diff_max, abweichung * Kp, v_max)

        # Einhalten der Mindestgeschwindigkeit
        geschwindigkeit = max(geschwindigkeit, v_min)

        # Zwischenspeichern der aktuellen Geschwindigkeit
        v_vor = geschwindigkeit

        # Ansteuern der Motoren
        motorR.run(-drehrichtung * geschwindigkeit)
        motorL.run(drehrichtung * geschwindigkeit)

    # Stoppen der Motoren nach Beendigung der Schleife
    motorR.hold()
    motorL.hold()



# ====================================
# Fahren mit Abstandsregelung zur Wand
# ====================================
def fahren_wand(geschwindigkeit:int, motorL:Motor, motorR:Motor, abstandssensor:UltrasonicSensor):
    """_summary_

    Args:
        geschwindigkeit (int): _description_
        motorL (Motor): _description_
        motorR (Motor): _description_
        abstandssensor (UltrasonicSensor): _description_
    """
    # ca. 9 cm ausgemessen, damit der Roboter mittig im Feld fährt
    sollabstand = 90
    verstaerkung = 1.6  

    wandabstand = abstandssensor.distance()
    fehler = sollabstand - wandabstand

    motorL.run(geschwindigkeit - verstaerkung * fehler)
    motorR.run(geschwindigkeit + verstaerkung * fehler)



def fahren_gerade_distanz(geschwindigkeit:int, motorR:Motor, motorL:Motor, distanz:float):
    """ Gerades Fahren über eine feste Distanz - ansteuern der Motoren mit: .run_angle(speed, rotation_angle, then=Stop.HOLD, wait=True)
        Dreht den Motor mit einer konstanten Geschwindigkeit um einen bestimmten Winkel

    Args:
        geschwindigkeit (int): Vorgabegeschwindigkeit für den Motor des Roboters in Grad/s
        motorR (Motor): Rechter Motor
        motorL (Motor): Linker Motor
        distanz (float): Fahrdistanz in cm 
    """
    # Die Fahrdistanz leitet sich aus dem Kreisumfang ab
    # distanz = 2 * pi * r * drehwinkel/360°        # in [cm]

    # Dabei ist r der Radius des Rades r = d/2 - Raddurchmesser = 5,5 cm
    r = 3 / 2                                     # in [cm]

    # Umstellen der Distanzgleichung nach dem Drehwinkel
    # drehwinkel = distanz * 350° / (2 * pi * r)
    drehwinkel = distanz * 360 / (2 * math.pi * r)  # in [°]

    # Bewegen der Motoren um den gewünschten Winkel
    # beim 1. Befehl wait = False, damit nicht gewartet wird bis der Befehl abgeschlossen wird und gleich der nächste begonnen wird
    motorR.run_angle(geschwindigkeit, drehwinkel, wait=False)
    motorL.run_angle(geschwindigkeit, drehwinkel)
    
    # motorR.run_angle(geschwindigkeit, drehwinkel, then=Stop.COAST, wait=False)
    # motorL.run_angle(geschwindigkeit, drehwinkel, then=Stop.COAST)




# ====================
# Flagge fallen lassen
# ====================
def flagge(drehwinkel:int, motorFlagge:Motor):
    motorFlagge.run_angle(300, drehwinkel)




# ====================
# Labyrinth bewältigen
# ====================
def labyrinth(geschwindigkeit:int, motorL:Motor, motorR:Motor, motorFlagge:Motor, abstandssensor:UltrasonicSensor, tastsensor:TouchSensor, gyro_sensor:GyroSensor, farbsensor:ColorSensor):
    """_summary_

    Args:
        motorL (Motor): _description_
        motorR (Motor): _description_
        abstandssensor (UltrasonicSensor): _description_
        tastsensor (TouchSensor): _description_
        gyro_sensor (GyroSensor): _description_
    """

    gangabstand = 125
    flaggenzaehler = 0

    while True:
        wait(50)
        # Farbsensor erkennt schwarz -> Ziel erreicht
        rgb = farbsensor.rgb()
        if rgb[0] < 17 and rgb[1] < 17 and rgb[2] < 17:
            print(rgb)
            stop(motorL, motorR)
            break

        # Tastsensor ausgelöst -> Wand vorne
        if tastsensor.pressed():
            stop(motorL, motorR)
            wait(100)

            # Zurückfahren, damit der Roboter wieder mittig im Feld steht
            # Ausgemessen ca.: 6,5 cm
            fahren_gerade_distanz(-geschwindigkeit, motorR, motorL, 6.6)
            # fahren_gerade(-geschwindigkeit, motorL, motorR)
            # wait(750)
            # stop(motorL, motorR)
            wait(50)

            drehen_gyro_reglerbasiert(motorL, motorR, gyro_sensor, 180, -1)
            wait(50)

            wandabstand = abstandssensor.distance()
            print(wandabstand)

            # Sackgasse
            if wandabstand < gangabstand:
                flaggenzaehler += 1
                flagge(90, motorFlagge)
                if flaggenzaehler == 2:
                    flagge(-180, motorFlagge)
            # keine Sackgasse - rechte Wand frei
            else:
                print("keine Sackgasse - rechte Wand frei")
                drehen_gyro_reglerbasiert(motorL, motorR, gyro_sensor, 90, 1)
                
                wait(50)
    

        wandabstand = abstandssensor.distance()

        # Hoher Wandabstand -> Rechts Wandeinbruch
        if wandabstand > gangabstand:
            fahren_gerade_distanz(geschwindigkeit, motorR, motorL, 16.2)
            # fahren_gerade(geschwindigkeit, motorL, motorR)
            # wait(1400)
            # stop(motorL, motorR)
            wait(50)

            drehen_gyro_reglerbasiert(motorL, motorR, gyro_sensor, 90, +1)
            wait(50)

            fahren_gerade_distanz(geschwindigkeit, motorR, motorL, 13)
            # fahren_gerade(geschwindigkeit, motorL, motorR)
            # wait(1000)
        else:
            fahren_wand(geschwindigkeit, motorL, motorR, abstandssensor)

    if flaggenzaehler == 1:
        flagge(-90, motorFlagge)





# =============================
# Methode zum Prüfen der Farben
# =============================
def farbtest(farbsensor:ColorSensor, tastsensor:TouchSensor, ev3:EV3Brick):
    """ Manuelle Methode zum Erfahren der aktuellen Referenzwerte 
        sowie zum Prüfen der Farbscan-Funktion

    Args:
        farbsensor ColorSensor): Farbsensor
        tastsensor (TouchSensor): Berührungssensor
        ev3 (EV3Brick): Microrechner

    Returns:
        tuple(tuple(int, int, int), int):
        - weisswert (tuple(int, int, int)): RGB-Referenzwerte des Weißabgleichs 
        - grauwert_mitte (int): Grauwert des mittleren Orientierungsstreifens
    """
    # Weisswert bestimmen - zur Normierung der Farbwerte
    # Ausgelöst durch betätigen des Tastsensors
    print("Scanne das weiße Blatt!")
    ev3.screen.print("Scanne das\n weiße Blatt!")
    ev3.speaker.beep()

    while True:
        while (not tastsensor.pressed()):
            pass
        weisswert = farbsensor.rgb()

        print("weisswert: %.1f, %.1f, %.1f" % (weisswert[0], weisswert[1], weisswert[2]))
        ev3.screen.print("weisswert:\n%.1f, %.1f, %.1f" % (weisswert[0], weisswert[1], weisswert[2]))
        ev3.speaker.beep()
        while (tastsensor.pressed()):
            pass






