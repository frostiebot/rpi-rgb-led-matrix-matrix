#!/home/chris/.virtualenvs/matrix/bin/python

import math
import time

from matrix import Matrix

matrix = Matrix(font_path='fonts/sonic-advance-16.bdf', double_buffer=True)

_current_time = lambda: time.strftime('%H:%M:%S')

w = matrix.text_width('88:88:88')
x = (matrix.width / 2) - (w / 2)
y = (matrix.height / 2) + (matrix.font.height / 2)

try:
  while True:
    matrix.clear()
    # w = matrix.text_width(_current_time())
    # x = (matrix.width / 2) - (w / 2)
    # y = (matrix.height / 2) + (matrix.font.height / 2)
    matrix.draw_text(x, y, _current_time(), (0, 128, 0), (0, 0, 0))
    matrix.swap_buffer()
except KeyboardInterrupt:
  print 'shutting down...'
