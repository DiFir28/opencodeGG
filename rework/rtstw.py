#!/usr/bin/env python3

import time
import math
from smbus2 import SMBus

def scan_i2c_bus():
    """Сканирование I2C шины"""
    print("🔍 Сканирование I2C шины...")
    try:
        bus = SMBus(1)
        devices = []
        for address in range(0x03, 0x78):
            try:
                bus.read_byte(address)
                devices.append(address)
            except:
                pass
        bus.close()
        
        if devices:
            print("✅ Найденные устройства:")
            for dev in devices:
                print(f"   - 0x{dev:02X}")
            return devices
        else:
            print("❌ Устройства не найдены!")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка сканирования: {e}")
        return []

class MPU6050:
    def __init__(self, bus_number=1, address=0x68):
        self.bus = SMBus(bus_number)
        self.address = address
        self.init_sensor()
    
    def init_sensor(self):
        """Инициализация MPU-6050/6500/9250"""
        try:
            # Выход из sleep mode
            self.bus.write_byte_data(self.address, 0x6B, 0x00)
            time.sleep(0.1)
            
            # Настройка гироскопа ±500 °/s
            self.bus.write_byte_data(self.address, 0x1B, 0x08)
            
            # Настройка акселерометра ±4g
            self.bus.write_byte_data(self.address, 0x1C, 0x08)
            
            # Настройка ФНЧ ~21 Hz
            self.bus.write_byte_data(self.address, 0x1A, 0x04)
            
            print(f"✅ MPU инициализирован на адресе 0x{self.address:02X}")
            
        except Exception as e:
            print(f"❌ Ошибка инициализации: {e}")
            raise
    
    def read_word_2c(self, reg):
        """Чтение 16-битного значения со знаком"""
        try:
            high = self.bus.read_byte_data(self.address, reg)
            low = self.bus.read_byte_data(self.address, reg + 1)
            value = (high <<  + low)
            if value >= 0x8000:
                value = -((65535 - value) + 1)
            return value
        except Exception as e:
            print(f"Ошибка чтения регистра 0x{reg:02X}: {e}")
            return 0
    
    def get_accel_data(self):
        """Получение данных акселерометра в m/s²"""
        scale = 4.0 / 32768.0 * 9.81  # для ±4g в m/s²
        x = self.read_word_2c(0x3B) * scale
        y = self.read_word_2c(0x3D) * scale
        z = self.read_word_2c(0x3F) * scale
        return x, y, z
    
    def get_gyro_data(self):
        """Получение данных гироскопа в rad/s"""
        scale = 500.0 / 32768.0 * (math.pi / 180.0)  # для ±500°/s в rad/s
        x = self.read_word_2c(0x43) * scale
        y = self.read_word_2c(0x45) * scale
        z = self.read_word_2c(0x47) * scale
        return x, y, z
    
    def get_temperature(self):
        """Получение температуры в °C"""
        temp_raw = self.read_word_2c(0x41)
        return (temp_raw / 340.0) + 36.53

class ComplementaryFilter:
    """Комплементарный фильтр для объединения акселерометра и гироскопа"""
    def __init__(self, alpha=0.98):
        self.alpha = alpha
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.last_time = time.monotonic()
    
    def update(self, accel_x, accel_y, accel_z, gyro_x, gyro_y):
        current_time = time.monotonic()
        dt = current_time - self.last_time
        if dt <= 0:
            dt = 0.01
        self.last_time = current_time
        
        # Углы из акселерометра (в радианах)
        accel_angle_x = math.atan2(accel_y, math.sqrt(accel_x**2 + accel_z**2))
        accel_angle_y = math.atan2(-accel_x, math.sqrt(accel_y**2 + accel_z**2))
        
        # Интегрирование гироскопа
        self.angle_x += gyro_x * dt
        self.angle_y += gyro_y * dt
        
        # Комплементарная фильтрация
        self.angle_x = self.alpha * self.angle_x + (1 - self.alpha) * accel_angle_x
        self.angle_y = self.alpha * self.angle_y + (1 - self.alpha) * accel_angle_y
        
        return math.degrees(self.angle_x), math.degrees(self.angle_y)
def main():
    print("🎯 Инициализация MPU-6050/6500/9250")
    print("=" * 50)
    
    # Сканируем шину
    devices = scan_i2c_bus()
    
    if not devices:
        print("\n⚠️  Проверьте:")
        print("   - Подключение питания (3.3V)")
        print("   - Подключение GND")
        print("   - Подключение SDA/SCL")
        print("   - Включен ли I2C (sudo raspi-config)")
        return
    
    # Пробуем оба возможных адреса
    addresses_to_try = [0x68, 0x69]
    mpu = None
    
    for addr in addresses_to_try:
        if addr in devices:
            print(f"🔄 Пробуем адрес 0x{addr:02X}...")
            try:
                mpu = MPU6050(address=addr)
                print(f"✅ Успешно подключено к адресу 0x{addr:02X}")
                break
            except Exception as e:
                print(f"❌ Не удалось подключиться к 0x{addr:02X}: {e}")
    
    if mpu is None:
        print("❌ Не удалось инициализировать датчик ни на одном адресе")
        return
    
    # Инициализируем фильтр
    comp_filter = ComplementaryFilter(alpha=0.98)
    
    print("\n🎯 Опрос начат. Нажмите Ctrl+C для остановки.")
    print("=" * 60)
    
    try:
        while True:
            # Чтение данных
            accel = mpu.get_accel_data()
            gyro = mpu.get_gyro_data()
            temp = mpu.get_temperature()
            
            # Применение фильтра
            roll, pitch = comp_filter.update(accel[0], accel[1], accel[2], gyro[0], gyro[1])
            
            # Вывод результатов
            print("\033[2J\033[H")  # Очистка консоли
            print("=== ДАННЫЕ MPU-6050/6500/9250 ===")
            print(f"📊 Акселерометр (m/s²):")
            print(f"   X: {accel[0]:7.3f}, Y: {accel[1]:7.3f}, Z: {accel[2]:7.3f}")
            
            print(f"🔄 Гироскоп (рад/с):")
            print(f"   X: {gyro[0]:7.3f}, Y: {gyro[1]:7.3f}, Z: {gyro[2]:7.3f}")
            
            print(f"🌡️  Температура: {temp:6.2f} °C")
            
            print(f"📐 Углы (фильтр):")
            print(f"   Крен: {roll:6.2f}°, Тангаж: {pitch:6.2f}°")
            print("-" * 50)
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Программа остановлена пользователем")
    finally:
        mpu.bus.close()

if __name__ == "__main__":
    main()
