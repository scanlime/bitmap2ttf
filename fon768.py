#!/usr/bin/env python
#
# Convert 768-byte 8x8 96-character fonts to WOFF
#
# This is a trivial importer by Micah Scott, based on library code
# from Alistair Buxton et al, and using Fontforge to craft the output file.
#
# Copyright 2018 Micah Elizabeth Scott <micah@misc.name>
#
# License: This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3 of the License, or (at
# your option) any later version. This program is distributed in the hope
# that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

import sys
from convert import convert

try:
    from PIL import Image
except ImportError:
    import Image

def render(font, index):
    im = Image.new('1', (8,8))
    for y in range(8):
        byte = font[y*0x60 + index]
        for x in range(8):
            if byte & (0x80 >> x):
                im.paste(1, (x, y, x+1, y+1))
    return im

def fontGlyphs(font):
    g = {}
    for i in range(0x60):
        g[0x20 + i] = render(font, i)
    return g

def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: %s input.fon output.(woff|ttf|...)\n" % sys.argv[0])
    else:
        # Rectangular pixels
        width_adjust = 388 * 4/3.0 / 644
        convert(fontGlyphs(open(sys.argv[1], 'rb').read()), sys.argv[2], par=width_adjust)

if __name__ == '__main__':
    main()
