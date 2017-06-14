#!/home/chris/.virtualenvs/matrix/bin/python

import math
import time

from matrix import Matrix

new_matrix = Matrix(font_path='fonts/sonic-advance-16.bdf', double_buffer=True, show_refresh=True, daemon=False)

class ColorCycler(object):
  def __init__(self):
    self.cycle = 0

  def next_rgb(self):
    self.cycle += 1
    self.cycle %= 3 * 255

    red = 0
    green = 0
    blue = 0

    if self.cycle <= 255:
      c = self.cycle
      blue = 255 - c
      red = c
    elif self.cycle > 255 and self.cycle <= 511:
      c = self.cycle - 256
      red = 255 - c
      green = c
    else:
      c = self.cycle - 512
      green = 255 - c
      blue = c

    return red, green, blue

text = u'\u00a92017 BuildIt Digital'

text_position = new_matrix.width
text_y = (new_matrix.height / 2) + (new_matrix.font.height / 2)

color_cycler = ColorCycler()

# pixel = 0
# max_pixel = new_matrix.width * new_matrix.height

try:
  while True:
      new_matrix.clear()

      x, y = new_matrix.XY_CENTER

      # new_matrix.draw_line(0, 0, new_matrix.width - 1, new_matrix.height - 1, (0, 128, 0))

      # new_matrix.draw_rectangle(1, 1, 62, 30, (32, 0, 0), False)
      # new_matrix.draw_filled_rectangle(1, 1, 62, 30, (32, 0, 0))  # NOT ANY MORE - draw_rectangle(..., fill=True)

      new_matrix.draw_circle(x - 1, y - 1, 11, (0, 32, 0), True)
      # new_matrix.draw_filled_circle(x - 1, y - 1, 11, (0, 32, 0))  # NOT ANY MORE - draw_circle(..., fill=True)

      # text_length = text_position

      # for glyph in text:
      #   r, g, b = color_cycler.next_rgb()
      #   text_length += new_matrix.draw_glyph(text_length, text_y, glyph, color_cycler.next_rgb())

      # text_length = text_length - text_position
      # text_position -= 1

      # if (text_position + text_length) < 0:
      #   text_position = new_matrix.width

      # time.sleep(0.05)

      new_matrix.swap_buffer()

except KeyboardInterrupt:
  print 'shutting down...'
