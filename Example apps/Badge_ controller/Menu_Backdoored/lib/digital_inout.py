import digitalio

# Internal helpers to simplify setting and getting a bit inside an integer.
def _get_bit(val, bit):
    return val & (1 << bit) > 0


class DigitalInOut:
    def __init__(self, pin_number, tca9539):
        self._pin = pin_number
        self._mcp = tca9539

    @property
    def value(self):
        return _get_bit(self._mcp.gpio, self._pin)

    @property
    def direction(self):
        return digitalio.Direction.OUTPUT