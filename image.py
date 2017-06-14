#!/home/chris/.virtualenvs/matrix/bin/python

from PIL import Image

from matrix import Matrix

matrix = Matrix(double_buffer=True)

try:
  im = Image.open('images/admiral-derpbar.png').convert('RGB')
  im = im.resize((matrix.width / 2, matrix.height), Image.ANTIALIAS)

  x, y = ((matrix.width / 2) - (im.width / 2)), 0

  matrix.set_image(im, x, y)
  matrix.swap_buffer()
  while True:
    pass
except KeyboardInterrupt:
  print 'shutting down...'
