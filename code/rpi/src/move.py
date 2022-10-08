from multiprocessing import Process
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import pigpio
import sys
import serial

#pins
base = 21
sholder = 16
elbow = 12
wrist = 20
wrist_2 = 25
gripper = 24
buzzer = 23
pi = pigpio.pi()
camera = PiCamera(resolution=(640, 480), framerate=24)

def lights(option):
  try:
    if option == "on":
      s = serial.Serial('/dev/ttyUSB0', 9600)
      time.sleep(2)
      s.write(b'1')
    elif option == "off":
      s = serial.Serial('/dev/ttyUSB0', 9600)
      time.sleep(2)
      s.write(b"0")
      s.close()
  except Exception:
    print("Check arduino connection!")

def start_camera():
  camera.rotation = 180
#  camera.start_recording('marker2.h264')
  camera.start_preview()

def stop_camera():
#  camera.stop_recording()
  camera.stop_preview()

def init():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(sholder, GPIO.OUT)
  GPIO.setup(elbow, GPIO.OUT)
  GPIO.setup(wrist, GPIO.OUT)
  GPIO.setup(buzzer, GPIO.OUT)

def make_buzzer_sound():
  GPIO.output(buzzer, 1)
  time.sleep(0.2)
  GPIO.output(buzzer, 0)

def move_base(base, direction):
  #cw = 1550
  #ccw = 1430
  pi.set_servo_pulsewidth(base, direction)
  prt = "sent pulse to {0}: value {1}".format(base, direction)
#  print(prt)

def move_joint(joint, from_pwm, to_pwm, reverse):

  if reverse == True:
    step = 5
  else:
    step = -5

  for pulse in range(from_pwm, to_pwm, step):
    pi.set_servo_pulsewidth(joint, pulse)
    time.sleep(0.01)
    prt = "sent pulse to {0}: {1}".format(joint, pulse)
#    print(prt)

  pi.set_servo_pulsewidth(joint, 0)
  prt = "sent pulse to {0}: {1}".format(joint, 0)
#  print(prt)

if __name__ == '__main__':

  #init
  init()
  lights("on")
  start_camera()
  counter = 0
  time.sleep(1)

  if len(sys.argv) > 1:
    reps = int(sys.argv[1])
  else:
   reps = 1

  while counter < reps:
    #buzzer
    make_buzzer_sound()

    #sholder
    s = Process(target=move_joint, args=(sholder, 2450, 2050, False))
    s.start()

    #elbow
    e = Process(target=move_joint, args=(elbow, 2400, 2000, False))
    e.start()

    #wrist
    w = Process(target=move_joint, args=(wrist, 2500, 1900, False))
    w.start()

    #base
    if counter%2 == 0:
      direction=1420
    else:
      direction=1560

    b = Process(target=move_base, args=(base, direction))
    b.start()
    b.join()

    time.sleep(2.5)

    b = Process(target=move_base, args=(base, 0))
    b.start()
    b.join()

    s.join()
    e.join()
    w.join()

    #buzzer
    make_buzzer_sound()

    #sholder
    s = Process(target=move_joint, args=(sholder, 2050, 2450, True))
    s.start()

    #elbow
    e = Process(target=move_joint, args=(elbow, 2000, 2400, True))
    e.start()

    #wrist
    w = Process(target=move_joint, args=(wrist, 1900, 2500, True))
    w.start()

    #base
    if counter%2 == 0:
      direction=1560
    else:
      direction=1420

    b = Process(target=move_base, args=(base, direction))
    b.start()
    b.join()

    time.sleep(2.5)

    b = Process(target=move_base, args=(base, 0))
    b.start()
    b.join()

    s.join()
    e.join()
    w.join()

    counter+=1

#end program with double buzzer
time.sleep(1)
lights("off")
stop_camera()
make_buzzer_sound()
time.sleep(0.1)
make_buzzer_sound()
