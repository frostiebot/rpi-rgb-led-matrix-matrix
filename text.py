#!/home/chris/.virtualenvs/matrix/bin/python

import math
import time
import argparse

from matrix import Matrix

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--text', action='store', help='Text to display', default=u'\u00a92017 BuildIt Digital', type=unicode)

args = parser.parse_args()

matrix = Matrix(font_path='fonts/sonic-advance-16.bdf', double_buffer=True)

text = args.text

try:
  w = matrix.draw_text(0, 0, text, (0, 0, 0))

  x = (matrix.width / 2) - (w / 2)
  y = (matrix.height / 2) + (matrix.font.height / 2)

  matrix.clear()

  matrix.draw_rectangle(
    (x - 1),
    ((y - matrix.font.height) + 1),
    ((x + w) - 1),
    y,
    (128, 0, 0),
    fill=True
  )
  matrix.draw_text(x, y, text, (0, 0, 0))

  matrix.swap_buffer()

  while True:
    pass
except KeyboardInterrupt:
  print 'shutting down...'
