import serial

def crc8(data: bytes):
    crc = 0x00
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc


ser = serial.Serial("/dev/ttyAMA4", 115200, timeout=1)

STATE_WAIT_HEADER = 0
STATE_LEN = 1
STATE_DATA = 2
STATE_CRC = 3

state = STATE_WAIT_HEADER
length = 0
buffer = bytearray()

while True:
    b = ser.read(1)
    if not b:
        continue

    byte = b[0]

    if state == STATE_WAIT_HEADER:
        if byte == 0xAA:
            state = STATE_LEN

    elif state == STATE_LEN:
        length = byte
        buffer = bytearray()
        state = STATE_DATA

    elif state == STATE_DATA:
        buffer.append(byte)
        if len(buffer) >= length:
            state = STATE_CRC

    elif state == STATE_CRC:
        recv_crc = byte
        calc_crc = crc8(buffer)

        if recv_crc == calc_crc:
            print("OK:", list(buffer))
        else:
            print("CRC ERROR")

        state = STATE_WAIT_HEADER