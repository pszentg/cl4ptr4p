import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(0o03, GPIO.OUT)

pwm = GPIO.PWM(0o03, 50)
pwm.start(0)


def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(0o03, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(0o03, False)
    pwm.ChangeDutyCycle(0)
