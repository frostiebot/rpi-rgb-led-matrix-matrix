#!/home/chris/.virtualenvs/matrix/bin/python

import math
import time
import argparse

from matrix import Matrix

'''
Nicer wave: -f 0.8 -a 0.25 -s 3.2
'''

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--frequency", action="store", help="Wave frequency. Default: 4.0", default=4.0, type=float)
parser.add_argument("-a", "--amplitude", action="store", help="Wave amplitude. Default: 0.25", default=0.25, type=float)
parser.add_argument("-s", "--speed", action="store", help="Speed of wave. Default: 1.0", default=1.0, type=float)

args = parser.parse_args()

matrix = Matrix(double_buffer=True)

center = matrix.height * 0.5

frequency = args.frequency  # 0.025  # 0.1
amplitude = matrix.height * args.amplitude # 0.25
speed = args.speed

try:
  while True:
    matrix.clear()
    for x in range(matrix.width):
      sy = center + amplitude * math.sin(frequency * ((float(x) / matrix.width) * (2 * math.pi) + (speed * time.time())))
      cy = center + amplitude * math.cos(frequency * ((float(x) / matrix.width) * (2 * math.pi) + (speed * time.time())))
      matrix.set_pixel(x, sy, 0, 255, 0)
      matrix.set_pixel(x, cy, 255, 0, 0)
    matrix.swap_buffer()
except KeyboardInterrupt:
  print 'shutting down...'
