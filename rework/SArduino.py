import serial
import time
import threading
import json
from Shared import therds_stop


with open('config.json', 'r', encoding='utf-8') as file:
     json = json.load(file)

ser = serial.Serial(
    port="/dev/ttyAMA4",
    baudrate=115200,    
    # parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,
    # bytesize=serial.EIGHTBITS,
    timeout=0.1            
)
msg_length =0
data= "lol"
gyro = 0

def crc8(data):
    crc = 0
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = ((crc << 1) ^ 0x07) & 0xFF if (crc & 0x80) else (crc << 1) & 0xFF
    return crc

# def read_from_arduino():
#     global data
#     global msg_length
#     global gyro
#     while True:
#         try:
#             if ser.in_waiting > 0:
#                 # Читаем сырые байты
#                 #print(msg_length)
#                 #echo_data = ser.read(2)
#                 raw_data = ser.readline()
                
#                 try:
#                     # Пробуем декодировать как UTF-8
#                     data = raw_data.decode('utf-8').rstrip()
#                     with threading.Lock():
#                         gyro = float(data)
#                         # print(gyro)
                    

#                     #print(f"Получено от Arduino: {data}")
#                     #print(f"SW ",end= "")
#                     # print(f"D",end= "")
#                 except UnicodeDecodeError:
#                     # Если не UTF-8, выводим hex
#                     hex_data = ' '.join(f'{x:02x}' for x in raw_data)
#                     print(f"S",end= "")
#         except Exception as e:
#             print(f"Ошибка чтения: {e}")
                
# def write_to_arduino(send):
#     global msg_length
#     message = send
#     encoded_msg = (message + '\n').encode('utf-8')
#     msg_length = int(len(encoded_msg))
#     ser.write(encoded_msg)
    



# if  __name__ == "__main__":
#     thread.start()

#     try:
#         while True:
#             pass
#         # Отправляем данные на Arduino
#             #message = input("Введите сообщение для Arduino (или 'exit' для выхода): ")
#             #if message.lower() == 'exit':
#              #   break
#             #encoded_msg = (message + '\n').encode('utf-8')
#             #msg_length = int(len(encoded_msg))
#             print(gyro,end="<-data\n")
    
#     # Отправляем данные
#             #ser.write((f',{0},{0},{0},{0},{10},\n').encode('utf-8'))
    
#     # Очищаем буфер от возможного эха
#         #if ser.in_waiting > 0:
#         # Читаем ровно столько байт, сколько отправили
#            # echo_data = ser.read(msg_length)
#             #print(f"Очищено эхо: {echo_data}") 
        
#     except KeyboardInterrupt:
#         print("\nПрограмма завершена")
#     finally:
#         ser.close()

def send(data: bytes):
    ser.write(bytes([0xAA, len(data)]) + data + bytes([crc8(data)]))

import struct

def send_int16_array(arr):
    data = struct.pack('<' + 'h' * len(arr), *arr)
    send(data)

# def read():
#     state, length, buf = 0, 0, bytearray()

#     while True:
#         b = ser.read(1)
#         if not b: return None
#         b = b[0]

#         if state == 0 and b == 0xAA: state = 1
#         elif state == 1: length, buf, state = b, bytearray(), 2
#         elif state == 2:
#             buf.append(b)
#             if len(buf) >= length: state = 3
#         elif state == 3:
#             return buf if crc8(buf) == b else None

def unpack_i16_array(buf: bytes):
    arr = []
    for i in range(0, len(buf), 2):
        val = int.from_bytes(buf[i:i+2], byteorder='little', signed=True)
        arr.append(val)
    return arr

def read_theard():
    global gyro
    global ser
    while not therds_stop.is_set():
        b = ser.read(1)
        
        while True:
            if b:                
                if b[0] == 0xAA:
                    break
            b = ser.read(1)
            
        
        b = ser.read(1)[0]
        length, buf = b, bytearray()
        for s in range(length):
            buf.append(ser.read(1)[0])
        recv_crc = ser.read(1)[0]
        if crc8(buf) == recv_crc:   
            gyro=(unpack_i16_array(buf)[0]/10000)      

            
    ser.close()

thread = threading.Thread(target=read_theard)
thread.daemon = True

        
def send_int16_array(arr):
    data = bytearray()
    for v in arr:
        data += v.to_bytes(2, 'little', signed=True)
    send(data)

# ser = serial.Serial("/dev/ttyAMA4", 115200, timeout=0.01)
if  __name__ == "__main__":
    thread.start()

    try:
        while True:
            print(gyro)
            send_int16_array([0,0,0,200,0])
            time.sleep(0.1)
            pass
        
    except KeyboardInterrupt:
        send_int16_array([0,0,0,0,0])
        therds_stop.set()
        print("\nПрограмма завершена")
