import ipaddress
import wifi
import rtc
import ssl
import socketpool
import time
import binascii
import board

import adafruit_requests
import adafruit_hashlib as hashlib

import terminalio
from adafruit_display_text import label

ssid = '<WIFI SSID>'
password = '<WIFI PSK>'

totp = [("Google", 'XXXXXX')]

# TODO: Once update RTC with WiFi, then keep using RTC
for network in wifi.radio.start_scanning_networks():
    print(network, network.ssid, network.channel)
wifi.radio.stop_scanning_networks()

print("joining network...")
print(wifi.radio.connect(ssid=ssid, password=password))
# the above gives "ConnectionError: Unknown failure" if ssid/passwd is wrong

print("my IP addr:", wifi.radio.ipv4_address)

print("pinging 1.1.1.1...")
ip1 = ipaddress.ip_address("1.1.1.1")
print("ip1:", ip1)
print("ping:", wifi.radio.ping(ip1))

radio = wifi.radio
pool = socketpool.SocketPool(radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC")
if response.status_code == 200:
    r = rtc.RTC()
    r.datetime = time.localtime(response.json()['unixtime'])
    print(f"System Time: {r.datetime}")
else:
    print("Setting time failed")

SHA1 = hashlib.sha1

# HMAC implementation, as hashlib/hmac wouldn't fit
# From https://en.wikipedia.org/wiki/Hash-based_message_authentication_code

def HMAC(k, m):
    SHA1_BLOCK_SIZE = 64
    KEY_BLOCK = k + (b'\0' * (SHA1_BLOCK_SIZE - len(k)))
    KEY_INNER = bytes((x ^ 0x36) for x in KEY_BLOCK)
    KEY_OUTER = bytes((x ^ 0x5C) for x in KEY_BLOCK)
    inner_message = KEY_INNER + m
    outer_message = KEY_OUTER + SHA1(inner_message).digest()
    return SHA1(outer_message)


def base32_decode(encoded):
    missing_padding = len(encoded) % 8
    if missing_padding != 0:
        encoded += '=' * (8 - missing_padding)
    encoded = encoded.upper()
    chunks = [encoded[i:i + 8] for i in range(0, len(encoded), 8)]

    out = []
    for chunk in chunks:
        bits = 0
        bitbuff = 0
        for c in chunk:
            if 'A' <= c <= 'Z':
                n = ord(c) - ord('A')
            elif '2' <= c <= '7':
                n = ord(c) - ord('2') + 26
            elif n == '=':
                continue
            else:
                raise ValueError("Not base32")
            # 5 bits per 8 chars of base32
            bits += 5
            # shift down and add the current value
            bitbuff <<= 5
            bitbuff |= n
            # great! we have enough to extract a byte
            if bits >= 8:
                bits -= 8
                byte = bitbuff >> bits  # grab top 8 bits
                bitbuff &= ~(0xFF << bits)  # and clear them
                out.append(byte)  # store what we got
    return out


def int_to_bytestring(i, padding=8):
    result = []
    while i != 0:
        result.insert(0, i & 0xFF)
        i >>= 8
    result = [0] * (padding - len(result)) + result
    return bytes(result)


def generate_otp(int_input, secret_key, digits=6):
    if int_input < 0:
        raise ValueError('input must be positive integer')
    hmac_hash = bytearray(
        HMAC(bytes(base32_decode(secret_key)),
             int_to_bytestring(int_input)).digest()
    )
    offset = hmac_hash[-1] & 0xf
    code = ((hmac_hash[offset] & 0x7f) << 24 |
            (hmac_hash[offset + 1] & 0xff) << 16 |
            (hmac_hash[offset + 2] & 0xff) << 8 |
            (hmac_hash[offset + 3] & 0xff))
    str_code = str(code % 10 ** digits)
    while len(str_code) < digits:
        str_code = '0' + str_code

    return str_code

display = board.DISPLAY

def display_screen(text):
    # Set text, font, and color
    font = terminalio.FONT
    color = 0x0000FF

    # Create the text label
    text_area = label.Label(font, text=text, color=color, scale=2)

    # Set the location
    text_area.x = 10
    text_area.y = 10

    # Show it
    display.show(text_area)

while True:
    for name, secret in totp:
        otp = generate_otp(time.time() // 30, secret)
        print(name + " OTP output: ", otp)  # serial debugging output
        display_screen(name + " OTP output: " + otp)  # serial debugging output
    time.sleep(1)