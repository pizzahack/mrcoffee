from time import sleep
import RPi.GPIO as GPIO
import random

GPIO.setwarnings(False)

DIR = 17
STEP = 27
I1 = 10
I2 = 22
MS2 = 9
MS1 = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(I1, GPIO.OUT)
GPIO.setup(I2, GPIO.OUT)
GPIO.setup(MS1, GPIO.OUT)
GPIO.setup(MS2, GPIO.OUT)

GPIO.output(I1, GPIO.LOW)
GPIO.output(I2, GPIO.LOW)

GPIO.output(MS1, GPIO.LOW)
GPIO.output(MS2, GPIO.LOW)

GPIO.output(DIR, 0)

for _ in range(4000):
  if _%2==0:
    GPIO.output(DIR, 1)
  else:
    GPIO.output(DIR, 0)
  r = random.randint(25,250)
  sleep_time = random.randint(3, 7)/1000
  for x in range(r):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(sleep_time)
    GPIO.output(STEP, GPIO.LOW)
    sleep(sleep_time)
  print(_, r, sleep_time)
  sleep(random.randint(1,3))


