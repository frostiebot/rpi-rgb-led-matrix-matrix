#!/home/chris/.virtualenvs/matrix/bin/python

import random

from matrix import (
  Matrix, colors,
)

matrix = Matrix(double_buffer=True)


class MatrixRain(object):
  def __init__(self, matrix, rain_colors=colors.Green, tail=4, growth_rate=4):
    self.matrix = matrix

    if not isinstance(rain_colors, list):
      rain_colors = [rain_colors]

    self.colors = rain_colors
    self.tail = tail
    self.growth_rate = growth_rate

    self._step = 0

    self.drops = [[] for x in range(self.matrix.width)]

  def _draw_drop(self, x, y, color):
    for i in range(self.tail):
      if y - i >= 0 and y - i < self.matrix.height:
        level = 255 - ((255 // self.tail) * i)
        self.matrix.set_pixel(x, y - i, colors.color_scale(color, level))

  def step(self, amount=1):
    self.matrix.swap_buffer()
    self.matrix.clear()

    for i in range(self.growth_rate):
      new_drop = random.randint(0, self.matrix.width - 1)
      color_idx = random.randint(0, len(self.colors) - 1)

      self.drops[new_drop].append((0, self.colors[color_idx]))

    for x in range(self.matrix.width):
      col = self.drops[x]

      if len(col) > 0:
        removals = []

        for y in range(len(col)):
          drop = col[y]

          if drop[0] < self.matrix.height:
            self._draw_drop(x, drop[0], drop[1])

          if drop[0] - (self.tail - 1) < self.matrix.height:
            drop = (drop[0] + 1, drop[1])
            self.drops[x][y] = drop
          else:
            removals.append(drop)

        for r in removals:
          self.drops[x].remove(r)

matrix_rain = MatrixRain(matrix, growth_rate=6)

try:
  while True:
    matrix_rain.step()
except KeyboardInterrupt:
  print 'shutting down...'
