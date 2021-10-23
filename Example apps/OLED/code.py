import board
import busio
import sh1106
from tca9539 import TCA9539


io_expander = TCA9539(board.I2C())
io_expander.vext_on(True)

# Create the I2C interface.
i2c = busio.I2C(board.I2C_SCL, board.I2C_SDA)

# Create the SH1106 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = sh1106.SH1106_I2C(128, 64, i2c)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
oled.pixel(1, 1, 1)
oled.show()

# # https://diyusthad.com/image2cpp
# with open('cat.bin', 'rb') as f:
#     data = bytearray(f.read())

# buffer = bytearray(((128 // 8) * 64) + 1)
# buffer[1:] = data