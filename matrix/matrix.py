# -*- coding: utf-8 -*-

import atexit
import time

import rgbmatrix

from rgbmatrix import graphics

from . import util


def _clear_matrix(matrix):
  matrix.clear()
  print 'RGB MATRIX DONE!'


class Matrix(object):
  def __init__(self, font_path=None, double_buffer=False, show_refresh=False, gpio_slowdown=1, scan_mode=0, pwm_bits=11, pwm_lsb_nanoseconds=130, disable_hardware_pulse=False, daemon=False):
    options = rgbmatrix.RGBMatrixOptions()

    options.hardware_mapping = 'adafruit-hat-pwm'
    options.rows = 32
    options.chain_length = 2
    options.parallel = 1

    options.show_refresh_rate = int(show_refresh)

    options.gpio_slowdown = gpio_slowdown
    options.pwm_bits = pwm_bits
    options.pwm_lsb_nanoseconds = pwm_lsb_nanoseconds

    options.scan_mode = scan_mode if scan_mode in range(2) else 1

    if disable_hardware_pulse:
      options.disable_hardware_pulsing = True

    options.daemon = daemon

    self.double_buffer = double_buffer

    self._matrix = rgbmatrix.RGBMatrix(options=options)
    self._frame_canvas = None
    self._font = None

    if font_path is not None:
      self.load_font(font_path)

    atexit.register(_clear_matrix, self)

  @property
  def font(self):
    if self._font:
      return self._font
    return None

  @property
  def canvas(self):
    if not self.double_buffer:
      return self._matrix
    if not self._frame_canvas:
      self._frame_canvas = self._matrix.CreateFrameCanvas()
    return self._frame_canvas

  @property
  def width(self):
    return self.canvas.width

  @property
  def height(self):
    return self.canvas.height

  @property
  def XY_CENTER(self):
    return ((self.canvas.width / 2) - 1), ((self.canvas.height / 2) - 1)

  def sleep(self, value):
    time.sleep(value / 1000000.0)

  def fill(self, color):
    self.canvas.Fill(*color)

  def clear(self):
    self.canvas.Clear()

  def set_pixel(self, x, y, color):
    self.canvas.SetPixel(x, y, *color)

  def set_pixel_at_address(self, i, color):
    x, y = divmod(i, self.canvas.height)
    self.set_pixel(x, y, *color)

  def set_image(self, image, offset_x=0, offset_y=0, unsafe=True):
    self.canvas.SetImage(image, offset_x, offset_y, unsafe)

  def set_pixels_pillow(self, image, x, y, width, height):
    self.canvas.SetPixelsPillow(x, y, width, height, image)

  def swap_buffer(self):
    if self.double_buffer:
      self._frame_canvas = self._matrix.SwapOnVSync(self._frame_canvas)

  def load_font(self, path):
    _font = graphics.Font()
    _font.LoadFont(path)
    self._font = _font

  def glyph_width(self, glyph):
    if self.font:
      if not isinstance(glyph, int):
        glyph = ord(glyph)
      return self.font.CharacterWidth(glyph)

  def text_width(self, text):
    return sum(map(self.glyph_width, text))

  def draw_text(self, x, y, text, color, background_color=(0, 0, 0)):
    if self.font:
      color = graphics.Color(*color)
      background_color = graphics.Color(*background_color)
      return graphics.DrawText(self.canvas, self.font, x, y, color, background_color, text)

  def draw_glyph(self, x, y, glyph, color, background_color=(0, 0, 0)):
    if self.font:
      if not isinstance(glyph, int):
        glyph = ord(glyph)
      color = graphics.Color(*color)
      background_color = graphics.Color(*background_color)
      return self.font.DrawGlyph(self.canvas, x, y, color, background_color, glyph)

  def draw_line(self, x0, y0, x1, y1, color, algorithm=None):
    if any([algorithm in ('wu' ,'bresenham')]):
      getattr(util, '{}_line'.format(algorithm))(self, x0, y0, x1, y1, color)
    else:
      graphics.DrawLine(self.canvas, x0, y0, x1, y1, graphics.Color(*color))

  def draw_circle(self, x, y, radius, color, fill=False):
    color = graphics.Color(*color)
    getattr(
      graphics,
      'Draw{}Circle'.format('Filled' if fill else '')
    )(self.canvas, x, y, radius, color)

  def draw_rectangle(self, x0, y0, x1, y1, color, fill=False):
    color = graphics.Color(*color)
    getattr(
      graphics,
      'Draw{}Rectangle'.format('Filled' if fill else '')
    )(self.canvas, x0, y0, x1, y1, color)
