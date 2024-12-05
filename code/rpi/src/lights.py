import serial
import time
import sys

if __name__ == '__main__':
  try:
    try:
      s = serial.Serial('/dev/ttyUSB0', 9600)
      time.sleep(2)
      if sys.argv[1] == "--on":
        s.write(b'1')
      elif sys.argv[1] == "--off":
        s.write(b'0')
    except IndexError:
        print("missing arg '--on' or --off")
    except Exception:
        print("Check arduino connection!")
  except KeyboardInterrupt:
      s.close()

