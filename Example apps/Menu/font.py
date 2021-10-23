from adafruit_bitmap_font import bitmap_font


space_font_back = bitmap_font.load_font("fonts/spacefont-back-32.pcf")
space_font_back.load_glyphs(b'SPACE')
space_font_front = bitmap_font.load_font("fonts/spacefont-front-32.pcf")
space_font_front.load_glyphs(b'COWS')