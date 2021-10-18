import board
from digitalio import DigitalInOut, Direction, Pull
import time


switch = DigitalInOut(board.SA_GPIO1)
switch.direction = Direction.INPUT

while True:
    print(switch.value)
    time.sleep(0.1)