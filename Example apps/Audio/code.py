import audiocore
import board
import audiobusio
from digitalio import DigitalInOut, Direction

# TODO: I2S is broken in CircuitPython 7 for ESP32S2

# Turn audio power on
audio_en = DigitalInOut(board.AUDIO_EN)
audio_en.direction = Direction.OUTPUT
audio_en.value = True

wave_file = open("rick.wav", "rb")
wave = audiocore.WaveFile(wave_file)

audio = audiobusio.I2SOut(bit_clock=board.IO34, word_select=board.IO35, data=board.IO33)
audio.play(wave)