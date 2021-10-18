import board
from digitalio import DigitalInOut, Direction
import time


switch = DigitalInOut(board.SA_GPIO1)
switch.direction = Direction.OUTPUT
switch.value = True