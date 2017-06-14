#!/home/chris/.virtualenvs/matrix/bin/python

import itertools

from PIL import Image, ImageSequence

from matrix import Matrix

matrix = Matrix(double_buffer=True)

def extract_animation_frames(image_path, size):
  with Image.open(image_path) as im:
    for frame in ImageSequence.Iterator(im):
      frame = frame.convert('RGB').resize(size, Image.ANTIALIAS)
      yield frame

try:
  frames = extract_animation_frames(
    'images/pac-ghost.gif',
    (matrix.width / 2, matrix.height)
  )

  matrix.swap_buffer()

  for frame in itertools.cycle(frames):
    x, y = ((matrix.width / 2) - (frame.width / 2)), 0
    matrix.set_image(frame, x, y)
    matrix.swap_buffer()
    matrix.sleep(28000)

except KeyboardInterrupt:
  print 'shutting down...'
