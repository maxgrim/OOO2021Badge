import time
import board
import adafruit_pcf8563

i2c_bus = board.I2C()
rtc = adafruit_pcf8563.PCF8563(i2c_bus)

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

# Set date / time
# t = time.struct_time((2021, 10, 13, 21, 38, 0, 0, -1, -1))
# rtc.datetime = t

while True:
    if rtc.datetime_compromised:
        print("RTC unset")
        time.sleep(1)  # wait a second
        continue
    else:
        print("RTC reports time is valid")

    t = rtc.datetime
    print(
        "The date is {} {}/{}/{}".format(
            days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
        )
    )

    print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
    time.sleep(1)  # wait a second