import math

from . import colors


def point_on_circle(cx, cy, radius, angle):
    """Calculates the coordinates of a point on a circle given the center point, radius, and angle"""
    angle = math.radians(angle) - (math.pi / 2)
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    return (
      getattr(math, 'ceil' if x < cx else 'floor')(x),
      getattr(math, 'ceil' if y < cy else 'floor')(y)
    )


# Bresenham's algorithm
def bresenham_line(matrix, x0, y0, x1, y1, color, colorFunc=None):
    """Draw line from point x0,y0 to x,1,y1. Will draw beyond matrix bounds."""
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)

    err = dx / 2

    if y0 < y1:
        ystep = 1
    else:
        ystep = -1

    count = 0
    for x in range(int(x0), int(x1) + 1):
        if colorFunc:
            color = colorFunc(count)
            count += 1

        if steep:
            # self.set(y0, x, color)
            matrix.set_pixel(y0, x, color)
        else:
            # self.set(x, y0, color)
            matrix.set_pixel(x, y0, color)

        err -= dy
        if err < 0:
            y0 += ystep
            err += dx
# END Bresenham's algorithm


# Xiaolin Wu's Line Algorithm
def wu_line(matrix, x0, y0, x1, y1, color, colorFunc=None):
    funcCount = [0]  # python2 hack since nonlocal not available

    def plot(x, y, level):
        c = color
        if colorFunc:
            c = colorFunc(funcCount[0])
            funcCount[0] += 1

        c = colors.color_scale(color, int(255 * level))
        # self.set(int(x), int(y), c)
        matrix.set_pixel(x, y, c)

    def ipart(x):
        return int(x)

    def fpart(x):
        return x - math.floor(x)

    def rfpart(x):
        return 1.0 - fpart(x)

    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx

    # handle first endpoint
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = xend  # this will be used in the main loop
    ypxl1 = ipart(yend)

    if steep:
        plot(ypxl1, xpxl1, rfpart(yend) * xgap)
        plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap)
    else:
        plot(xpxl1, ypxl1, rfpart(yend) * xgap)
        plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap)

    # first y-intersection for the main loop
    intery = yend + gradient

    # handle second endpoint
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = xend  # this will be used in the main loop
    ypxl2 = ipart(yend)

    if steep:
        plot(ypxl2, xpxl2, rfpart(yend) * xgap)
        plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap)
    else:
        plot(xpxl2, ypxl2, rfpart(yend) * xgap)
        plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap)

    # main loop
    for x in range(int(xpxl1 + 1), int(xpxl2)):
        if steep:
            plot(ipart(intery), x, rfpart(intery))
            plot(ipart(intery) + 1, x, fpart(intery))
        else:
            plot(x, ipart(intery), rfpart(intery))
            plot(x, ipart(intery) + 1, fpart(intery))
        intery = intery + gradient

# END Xiaolin Wu's Line Algorithm
