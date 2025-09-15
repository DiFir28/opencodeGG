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
gyro = 0

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
    read_thread = threading.Thread(target=read_from_arduino)
    read_thread.daemon = True
    read_thread.start()

    try:
        while True:
            pass
        # Отправляем данные на Arduino
            #message = input("Введите сообщение для Arduino (или 'exit' для выхода): ")
            #if message.lower() == 'exit':
             #   break
            #encoded_msg = (message + '\n').encode('utf-8')
            #msg_length = int(len(encoded_msg))
            print(data,end="<-data\n")
    
    # Отправляем данные
            #ser.write((f',{0},{0},{0},{0},{10},\n').encode('utf-8'))
    
    # Очищаем буфер от возможного эха
        #if ser.in_waiting > 0:
        # Читаем ровно столько байт, сколько отправили
           # echo_data = ser.read(msg_length)
            #print(f"Очищено эхо: {echo_data}") 
        
    except KeyboardInterrupt:
        print("\nПрограмма завершена")
    finally:
        ser.close()
