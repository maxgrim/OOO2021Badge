import audiocore
import board
import audiobusio
from digitalio import DigitalInOut, Direction
from io_expander import IOExpander

# TODO: I2S is broken in CircuitPython 7 for ESP32S2 for now we use CircuitPython 6
#Button handler
io_expander = IOExpander(board.I2C())
# Turn audio power on
audio_en = DigitalInOut(board.AUDIO_EN)
audio_en.direction = Direction.OUTPUT
audio_en.value = True

wave_file = open("rick.wav", "rb")
wave = audiocore.WaveFile(wave_file)
def play_sound():
    audio = audiobusio.I2SOut(bit_clock=board.I2S_CLK, word_select=board.I2S_WS, data=board.I2S_DATA)
    audio.play(wave)

def main():
    io_expander.update()
    if io_expander.button_menu.fell:
        return
