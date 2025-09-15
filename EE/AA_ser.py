#!/usr/bin/env python3
import serial
import time
import threading


ser = serial.Serial(
    port='/dev/serial0',  # Используем UART пины GPIO
    baudrate=115200,     # Высокая скорость для минимизации задержек
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1            # Таймаут чтения (секунды)
)
msg_length =0
data= "lol"

def read_from_arduino():
    global data
    global msg_length
    while True:
        try:
            if ser.in_waiting > 0:
                # Читаем сырые байты
                #print(msg_length)
                #echo_data = ser.read(2)
                raw_data = ser.readline()
                print("DATAAAAA")
                
                try:
                    # Пробуем декодировать как UTF-8
                    data = raw_data.decode('utf-8').rstrip()
                    #print(f"Получено от Arduino: {data}")
                    #print(f"SW ",end= "")
                except UnicodeDecodeError:
                    # Если не UTF-8, выводим hex
                    hex_data = ' '.join(f'{x:02x}' for x in raw_data)
                    print(f"SE ",end= "")
        except Exception as e:
            print(f"Ошибка чтения: {e}")
                
def write_to_arduino(send):
    global msg_length
    message = send
    encoded_msg = (message + '\n').encode('utf-8')
    msg_length = int(len(encoded_msg))
    ser.write(encoded_msg)
    



if  __name__ == "__main__":
    
    try:
        while True:
            print(ser.in_waiting )
        
    except KeyboardInterrupt:
        print("\nПрограмма завершена")
    finally:
        ser.close()
