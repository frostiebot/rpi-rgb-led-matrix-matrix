#!/home/chris/.virtualenvs/matrix/bin/python
#
import math
import time

from matrix import (
  Matrix,
  colors,
  point_on_circle,
)

matrix = Matrix(double_buffer=True)

class AnalogClock(object):
  def __init__(self, matrix):
    self.matrix = matrix

    self.x = (matrix.width - 1) / 2
    self.y = (matrix.height - 1) / 2

    self.hand_length = self.x if self.x <= self.y else self.y
    self.hand_length -= 2

    self._hand_lengths = (self.hand_length * 0.7, self.hand_length * 0.8, self.hand_length * 0.9)
    self._hand_colors = (colors.Red, colors.Green, colors.Blue)

  def clock_hands(self):
    xy = (self.x, self.y)
    hour, minute, second = map(int, time.strftime('%I %M %S').split())

    for idx, hand in enumerate(
      zip(self._hand_lengths, ((hour * 30), (minute * 6), (second * 6)))
    ):
      yield xy + point_on_circle(*(xy + hand)) + (self._hand_colors[idx],)

  def tick(self):
    self.matrix.swap_buffer()
    self.matrix.clear()
    self.matrix.draw_circle(self.x, self.y, self.hand_length, colors.Cornsilk)
    for hand in self.clock_hands():
      args = hand + ('wu',)
      self.matrix.draw_line(*args)

analog_clock = AnalogClock(matrix)

try:
  while True:
    analog_clock.tick()
except KeyboardInterrupt:
  print 'shutting down...'
