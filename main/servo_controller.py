import RPi.GPIO as GPIO
from time import sleep


class ServoController:

    def __init__(self, servo):
        # SG90 has a duty threshold of 3-11%

        self.servo = servo
        self.alignment = 1

        # GPIO.BOARD would be the to-go if I had a very old Pi.
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(17, GPIO.OUT)

        # SG90 works with 50Hz
        self.pwm = GPIO.PWM(17, 50)
        self.pwm.start(self.servo.CENTER.value)

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()

    # SG90 isn't very precise, rotates 90 degrees both direction, so let's try with 5 degree steps
    def set_angle(self, angle):
        # easier to think with +/- 90 degrees, but to do the maths it's better to do 0-180
        angle += 90
        # divide 180 degrees with the 8% duty window, 22.5 degrees = 1% duty
        duty = angle / 22.5 + self.servo.MIN_DUTY.value
        if duty > self.servo.MAX_DUTY.value:
            duty = self.servo.MAX_DUTY.value
        if duty < self.servo.MIN_DUTY.value:
            duty = self.servo.MIN_DUTY.value
        GPIO.output(17, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(17, False)
        self.pwm.ChangeDutyCycle(0)

    def switch_on(self):
        self.set_angle(60)

    def switch_off(self):
        self.set_angle(-60)

