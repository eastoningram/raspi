 # Write your code here :-)
# System imports
import RPi.GPIO as GPIO
from time import sleep
import threading

# Keypress
import sys
import tty
import termios

import serial


def get_key_press():
    fd = sys.stdin.fileno()  # Get the file descriptor for standard input
    old_settings = termios.tcgetattr(fd)  # Save the current terminal settings
    try:
        tty.setraw(fd)  # Set the terminal to raw mode
        ch = sys.stdin.read(1)  # Read a single character
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restore the terminal settings
    return ch


forwards = True

def my_callback(channel):
    global forwards
    forwards = not forwards
    print(forwards)
    sleep(.1)

class StepperHandler():

    __CLOCKWISE = 1
    __ANTI_CLOCKWISE = 0

    def __init__(self, stepPin, directionPin, delay=0.208, stepsPerRevolution=200):

        # Configure instance
        self.CLOCKWISE = self.__CLOCKWISE
        self.ANTI_CLOCKWISE = self.__ANTI_CLOCKWISE
        self.StepPin = stepPin
        self.DirectionPin = directionPin
        self.Delay = delay
        self.RevolutionSteps = stepsPerRevolution
        self.CurrentDirection = self.CLOCKWISE
        self.CurrentStep = 0

        # Setup gpio pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.StepPin, GPIO.OUT)
        GPIO.setup(self.DirectionPin, GPIO.OUT)


    def Step(self, stepsToTake, direction = __CLOCKWISE):

#        print("Step Pin: " + str(self.StepPin) + " Direction Pin: " + str(self.DirectionPin) + " Delay: " + str(self.Delay))
#        print("Taking " + str(stepsToTake) + " steps.")

        # Set the direction
        GPIO.output(self.DirectionPin, direction)

        # Take requested number of steps
        for x in range(stepsToTake):
            #print("Step " + str(x))
            GPIO.output(self.StepPin, GPIO.HIGH)
            self.CurrentStep += 1
            sleep(self.Delay)
            GPIO.output(self.StepPin, GPIO.LOW)
            sleep(self.Delay)
def t1():
    stepperHandler1.Step(100)

def t2():
    stepperHandler2.Step(100, stepperHandler2.ANTI_CLOCKWISE)

def t3():
    stepperHandler1.Step(100, stepperHandler1.ANTI_CLOCKWISE)

def t4():
    stepperHandler2.Step(100)


def t5():
    GPIO.output(SLEEP_PIN1, GPIO.LOW)

def t6():
    GPIO.output(SLEEP_PIN2, GPIO.LOW)


# Define pins
STEP_PIN1 = 16
DIRECTION_PIN1 = 21
SLEEP_PIN1 = 20
STEP_PIN2 = 5
DIRECTION_PIN2 = 6
SLEEP_PIN2 = 13
POWER_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(SLEEP_PIN1, GPIO.OUT)
GPIO.setup(SLEEP_PIN2, GPIO.OUT)
GPIO.setup(POWER_PIN, GPIO.OUT)
GPIO.output(SLEEP_PIN1, GPIO.HIGH)
GPIO.output(SLEEP_PIN2, GPIO.HIGH)

GPIO.output(SLEEP_PIN1, GPIO.LOW)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

# Create a new instance of our stepper class (note if you're just starting out with this you're probably better off using a delay of ~0.1)
stepperHandler1 = StepperHandler(STEP_PIN1, DIRECTION_PIN1, 0.001)

stepperHandler2 = StepperHandler(STEP_PIN2, DIRECTION_PIN2, 0.001)

#GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.remove_event_detect(23)
#GPIO.add_event_detect(23,GPIO.FALLING,callback=my_callback,bouncetime=300)


while(True):
    # Wait for a key press
    user_input = get_key_press()

    GPIO.output(SLEEP_PIN1, GPIO.HIGH)
    GPIO.output(SLEEP_PIN2, GPIO.HIGH)
    if (user_input=="w"):
        thr1=threading.Thread(target=t1)
        thr2=threading.Thread(target=t2)

    elif (user_input=="s"):
        thr1=threading.Thread(target=t3)
        thr2=threading.Thread(target=t4)

    elif (user_input=="d"):
        thr1=threading.Thread(target=t3)
        thr2=threading.Thread(target=t2)

    elif (user_input=="a"):
        thr1=threading.Thread(target=t1)
        thr2=threading.Thread(target=t4)


    elif (user_input == "x"):
        break

    else:
        thr1=threading.Thread(target=t5)
        thr2=threading.Thread(target=t6)

    thr1.start()
    thr2.start()
    thr1.join()
    thr2.join()

    #GPIO.output(POWER_PIN, GPIO.HIGH)
    #sleep(.01)
    line = ser.readline().decode('utf-8').rstrip()
    power_read=int(line)
    battery_percent=(1-(651.0-power_read)/(615.0-496.0))*100
    print("Battery: " + "{:.1f}".format(battery_percent) + "%")
    #sleep(.01)
    #GPIO.output(POWER_PIN, GPIO.LOW)

GPIO.output(SLEEP_PIN1, GPIO.LOW)
GPIO.output(SLEEP_PIN2, GPIO.LOW)
# Go forwards once
#try:
#    while(True):
#        if (forwards):
#            forwards=False
            #stepperHandler2.Step(100, stepperHandler2.ANTI_CLOCKWISE)
#        else:
#                        forwards=True
#except KeyboardInterrupt:
GPIO.cleanup()
