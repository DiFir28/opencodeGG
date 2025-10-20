#!/usr/bin/env python3
import serial
import time
import threading
import json
import struct

with open('config.json', 'r', encoding='utf-8') as file:
     json = json.load(file)

ser = serial.Serial(
    port=json['Serial port'],
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

msg_length =0
data= ""

def crc8(data: bytes) -> int:
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc

def send_packet(ser, cmd: int, payload: bytes):
    length = len(payload) + 1            # LEN = len(DATA) + CRC
    crc = crc8(bytes([length]) + payload)  # CRC from LEN + DATA
    packet = bytes([0xAA, length]) + payload + bytes([crc])
    ser.write(packet)
    # print("Sent:", packet.hex(' '))

def read_packet(ser):
    if ser.read(1) != b'\xAA':
        return None
    length = ser.read(1)
    if not length:
        return None
    length = length[0]
    body = ser.read(length)
    if len(body) != length:
        return None
    crc = body[-1]
    calc_crc = crc8(bytes([length]) + body[:-1])
    if crc != calc_crc:
        print("CRC error!")
        return None
    data = body[:-1]
    return (data)


def read():
    global data
    global msg_length
    while True:
        try:
            if ser.in_waiting > 0:
                # Читаем сырые байты
                #print(msg_length)
                #echo_data = ser.read(2)
                raw_data = ser.readline()
                print(raw_data)
                
                # try:
                #     # Пробуем декодировать как UTF-8
                #     data = raw_data.decode('utf-8').rstrip()
                #     #print(f"Получено от Arduino: {data}")
                #     #print(f"SW ",end= "")
                # except UnicodeDecodeError:
                #     # Если не UTF-8, выводим hex
                #     hex_data = ' '.join(f'{x:02x}' for x in raw_data)
                #     print(f"SE ",end= "")
        except Exception as e:
            
            print(f"Ошибка чтения: {e}")
            # echo_data = ser.read(1)
                
def send(speed, ang, rot, drib, kick, rot_limit):
    # global msg_length
    # message = send
    # encoded_msg = (message + '\n').encode('utf-8')
    # msg_length = int(len(encoded_msg))
    # ser.write(encoded_msg)

    packet = struct.pack('<HHHHHH', speed, ang, rot, drib, kick, rot_limit)
    ser.write(packet)




if  __name__ == "__main__":
    
    try:
        send(500,2,3,4,5,6)
        read_thread = threading.Thread(target=read)
        read_thread.daemon = True
        read_thread.start()
        time.sleep(2)
        t_s = time.time()
        
        while (time.time() - t_s) <= 4:
            send(88,0,0,77,0,1)
            time.sleep(0.1)
            
            
        

            
        
    except KeyboardInterrupt:
        print("\nПрограмма завершена")
    finally:
        ser.close()
