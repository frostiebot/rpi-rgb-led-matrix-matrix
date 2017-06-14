#!/home/chris/.virtualenvs/matrix/bin/python

import math

from matrix import Matrix

matrix = Matrix(double_buffer=True)

def rotate(x, y, angle):
  return (x * math.cos(angle) - y * math.sin(angle)), (x * math.sin(angle) + y * math.cos(angle))
  # return {
  #     "new_x": x * math.cos(angle) - y * math.sin(angle),
  #     "new_y": x * math.sin(angle) + y * math.cos(angle)
  # }

def scale_col(val, lo, hi):
  if val < lo:
    return 0
  if val > hi:
    return 255
  return 255 * (val - lo) / (hi - lo)

def run():
  cent_x = matrix.width / 2
  cent_y = matrix.height / 2

  rotate_square = min(matrix.width, matrix.height) * 1.41
  min_rotate = cent_x - rotate_square / 2
  max_rotate = cent_x + rotate_square / 2

  display_square = min(matrix.width, matrix.height) * 0.7
  min_display = cent_x - display_square / 2
  max_display = cent_x + display_square / 2

  deg_to_rad = 2 * 3.14159265 / 360
  rotation = 0

  while True:
    rotation += 1
    rotation %= 360

    matrix.swap_buffer()

    for x in range(int(min_rotate), int(max_rotate)):
      for y in range(int(min_rotate), int(max_rotate)):
        rot_x, rot_y = rotate(x - cent_x, y - cent_x, deg_to_rad * rotation)

        if x >= min_display and x < max_display and y >= min_display and y < max_display:
          matrix.set_pixel(
            rot_x + cent_x,
            rot_y + cent_y,
            (
              scale_col(x, min_display, max_display),
              255 - scale_col(y, min_display, max_display),
              scale_col(y, min_display, max_display),
            )
          )
        else:
          matrix.set_pixel(rot_x + cent_x, rot_y + cent_y, (0, 0, 0))

try:
  run()
except KeyboardInterrupt:
  print 'shutting down...'
