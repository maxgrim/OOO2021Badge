import adafruit_imageload
import displayio


def load_logo():
    logo, logo_p = adafruit_imageload.load("/img/logo.bmp",
        bitmap=displayio.Bitmap,
        palette=displayio.Palette)

    logo_p.make_transparent(1)

    return (logo, logo_p)

def display_logo(group, logo_tuple, x, y):
    logo_grid = displayio.TileGrid(
        logo_tuple[0],
        pixel_shader=logo_tuple[1],
    )

    logo_grid.x = x
    logo_grid.y = y

    group.append(logo_grid)
