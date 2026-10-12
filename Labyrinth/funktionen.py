# Hier werden die erforderlichen Software-Module importiert.
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, GyroSensor, UltrasonicSensor)
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.parameters import Port, Stop, Direction, Button, Color
import time



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
    toleranz = 1 # [Grad]
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
    sollabstand = 100
    verstaerkung = 10

    wandabstand = abstandssensor.distance()

    motorL.run(min(geschwindigkeit, geschwindigkeit - (verstaerkung * (sollabstand - wandabstand))))
    motorR.run(min(geschwindigkeit, geschwindigkeit - (verstaerkung * (sollabstand - wandabstand))))




# ====================
# Labyrinth bewältigen
# ====================
def labyrinth():
    pass




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






