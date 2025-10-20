import smbus2

bus = smbus2.SMBus(1)
address = 0x68

who_am_i = bus.read_byte_data(address, 0x75)
print(f"WHO_AM_I: 0x{who_am_i:X}")