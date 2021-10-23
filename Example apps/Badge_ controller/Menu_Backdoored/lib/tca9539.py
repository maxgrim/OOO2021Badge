from micropython import const
import adafruit_bus_device.i2c_device as i2c_device
from digital_inout import DigitalInOut


_TCA9539_ADDR = const(0x74)
_TCA9539_GPIO_INPUT = const(0x00)
_TCA9539_GPIO_OUTPUT = const(0x02)
_TCA9539_CONFIG = const(0x06)

_OUT_BUFFER = bytearray(1)
_IN_BUFFER = bytearray(2)

_CONFIG_REGISTER = bytearray(3)
_VALUE_REGISTER = bytearray(2)


# outputs
# 2 vext_en

# special
# 7 lpad_det

# buttons
# 3 rtrig
# 4 a
# 5 b
# 6 select
# 8 ltrig
# 9 down
# 10 center
# 11 left
# 12 up
# 13 right
# 14 start
# 15 menu


class TCA9539:
    def __init__(self, i2c, address=_TCA9539_ADDR):
        self._device = i2c_device.I2CDevice(i2c, address)
        self.gpio_cache = 0

        _CONFIG_REGISTER[0] = _TCA9539_CONFIG
        _CONFIG_REGISTER[1] = 0x2
        _CONFIG_REGISTER[2] = 0x0

        self._device.write(_CONFIG_REGISTER)

    def get_pin(self, pin):
        if not 0 <= pin <= 16:
            raise ValueError("Pin number must be 0-16.")
        return DigitalInOut(pin, self)

    @property
    def gpio(self):
        return self.gpio_cache

    def gpio_update(self):
        self.gpio_cache = self._read_u16le(_TCA9539_GPIO_INPUT)

    def _read_u16le(self, register):
        # Read an unsigned 16 bit little endian value from the specified 8-bit
        # register.
        _OUT_BUFFER[0] = register

        with self._device as bus_device:
            bus_device.write_then_readinto(_OUT_BUFFER, _IN_BUFFER, out_end=1, in_end=2)
        return (_IN_BUFFER[1] << 8) | _IN_BUFFER[0]

    def vext_on(self, value):
        # Then write value
        if value:
            pass
            # _valueRegister = _valueRegister | (1 << pin);    // and OR bit in register
        else:
            pass
            # _valueRegister = _valueRegister & ~(1 << pin);    // AND all bits

        # I2CSetValue(_address, _TCA9539_GPIO_OUTPUT    , _valueRegister_low);
        # I2CSetValue(_address, _TCA9539_GPIO_OUTPUT + 1, _valueRegister_high);