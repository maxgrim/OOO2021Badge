import audiocore
import board
import audiobusio
from digitalio import DigitalInOut, Direction
from io_expander import IOExpander


def main():
    io_expander = IOExpander(board.I2C())

    # Turn audio power on
    audio_en = DigitalInOut(board.AUDIO_EN)
    audio_en.direction = Direction.OUTPUT
    audio_en.value = True

    wave_file = open("rick.wav", "rb")
    wave = audiocore.WaveFile(wave_file)

    audio = audiobusio.I2SOut(bit_clock=board.I2S_CLK, word_select=board.I2S_WS, data=board.I2S_DATA)
    audio.play(wave)

    io_expander.update()
    if io_expander.button_menu.fell:
        return
