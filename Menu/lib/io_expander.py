from micropython import const
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_debouncer import Debouncer
import digitalio


_TCA9539_ADDR = const(0x74)
_TCA9539_GPIO_INPUT = const(0x00)
_TCA9539_GPIO_OUTPUT = const(0x02)
_TCA9539_CONFIG = const(0x06)

_OUT_BUFFER = bytearray(1)
_IN_BUFFER = bytearray(2)

# Configure P02 as an output
_CONFIG_REGISTER = bytearray(4)
_CONFIG_REGISTER[0] = _TCA9539_CONFIG
_CONFIG_REGISTER[1] = 0b11111011
_CONFIG_REGISTER[2] = _TCA9539_CONFIG + 1
_CONFIG_REGISTER[3] = 0b11111111

# By default everything is off
_GPIO_OUTPUT_REGISTER = bytearray(4)
_GPIO_OUTPUT_REGISTER[0] = _TCA9539_GPIO_OUTPUT
_GPIO_OUTPUT_REGISTER[1] = 0b00000000
_GPIO_OUTPUT_REGISTER[2] = _TCA9539_GPIO_OUTPUT + 1
_GPIO_OUTPUT_REGISTER[3] = 0b00000000

PIN_OUTPUT_VEXT_EN = const(2)
PIN_BUTTON_RTRIGGER = const(3)
PIN_BUTTON_A = const(4)
PIN_BUTTON_B = const(5)
PIN_BUTTON_SELECT = const(6)
PIN_BUTTON_LTRIGGER = const(8)
PIN_BUTTON_DOWN = const(9)
PIN_BUTTON_CENTER = const(10)
PIN_BUTTON_LEFT = const(11)
PIN_BUTTON_UP = const(12)
PIN_BUTTON_RIGHT = const(13)
PIN_BUTTON_START = const(14)
PIN_BUTTON_MENU = const(15)


class DigitalInOut:
    def __init__(self, pin_number, tca9539):
        self._pin = pin_number
        self._mcp = tca9539

    def get_bit(self, val, bit):
        return val & (1 << bit) > 0

    @property
    def value(self):
        return self.get_bit(self._mcp.gpio_cache, self._pin)

    @property
    def direction(self):
        return digitalio.Direction.OUTPUT


class IOExpander:
    def __init__(self, i2c, address=_TCA9539_ADDR):
        self._device = i2c_device.I2CDevice(i2c, address)
        self.gpio_cache = 0

        # Set default input/outputs
        with self._device as device:
            device.write(_CONFIG_REGISTER, start=0, end=2)
            device.write(_CONFIG_REGISTER, start=2, end=4)

        self.button_rtrigger = Debouncer(self.get_pin(PIN_BUTTON_RTRIGGER))
        self.button_a = Debouncer(self.get_pin(PIN_BUTTON_A))
        self.button_b = Debouncer(self.get_pin(PIN_BUTTON_B))
        self.button_select = Debouncer(self.get_pin(PIN_BUTTON_SELECT))
        self.button_ltrigger = Debouncer(self.get_pin(PIN_BUTTON_LTRIGGER))
        self.button_down = Debouncer(self.get_pin(PIN_BUTTON_DOWN))
        self.button_center = Debouncer(self.get_pin(PIN_BUTTON_CENTER))
        self.button_left = Debouncer(self.get_pin(PIN_BUTTON_LEFT))
        self.button_up = Debouncer(self.get_pin(PIN_BUTTON_UP))
        self.button_right = Debouncer(self.get_pin(PIN_BUTTON_RIGHT))
        self.button_start = Debouncer(self.get_pin(PIN_BUTTON_START))
        self.button_menu = Debouncer(self.get_pin(PIN_BUTTON_MENU))

        self.button_list = [
            self.button_rtrigger, self.button_a, self.button_b,
            self.button_select, self.button_ltrigger,
            self.button_down, self.button_center,
            self.button_left, self.button_up,
            self.button_right, self.button_start, self.button_menu
        ]

    def get_pin(self, pin):
        if not 0 <= pin <= 16:
            raise ValueError("Pin number must be 0-16.")
        return DigitalInOut(pin, self)

    @property
    def any_button_fell(self):
        for button in self.button_list:
            if button.fell:
                return True
        return False

    def update(self):
        self.gpio_cache = self._read_u16le(_TCA9539_GPIO_INPUT)
        for button in self.button_list:
            button.update()

    def _read_u16le(self, register):
        # Read an unsigned 16 bit little endian value from the specified 8-bit
        # register.
        _OUT_BUFFER[0] = register

        with self._device as bus_device:
            bus_device.write_then_readinto(_OUT_BUFFER, _IN_BUFFER, out_end=1, in_end=2)
        return (_IN_BUFFER[1] << 8) | _IN_BUFFER[0]

    def vext_on(self, value):
        if value:
            _GPIO_OUTPUT_REGISTER[1] = 0b00000100
        else:
            _GPIO_OUTPUT_REGISTER[1] = 0b00000000
        
        with self._device as device:
            device.write(_GPIO_OUTPUT_REGISTER, start=0, end=2)
            device.write(_GPIO_OUTPUT_REGISTER, start=2, end=4)
