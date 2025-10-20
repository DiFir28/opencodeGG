import smbus
import time
import math

# === Настройки ===
MPU_ADDR = 0x68      # Адрес MPU6050
bus = smbus.SMBus(1) # Для Raspberry Pi 4

# === Инициализация ===
def mpu_init():
    bus.write_byte_data(MPU_ADDR, 0x6B, 0)  # Вывод из sleep mode
    bus.write_byte_data(MPU_ADDR, 0x1C, 0)  # ±2g
    bus.write_byte_data(MPU_ADDR, 0x1B, 0)  # ±250°/s
    print("MPU6050 инициализирован")

def read_word(reg):
    high = bus.read_byte_data(MPU_ADDR, reg)
    low = bus.read_byte_data(MPU_ADDR, reg + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        val = -((65535 - val) + 1)
    return val

def read_accel_gyro():
    accel_x = read_word(0x3B)
    accel_y = read_word(0x3D)
    accel_z = read_word(0x3F)
    gyro_x = read_word(0x43)
    gyro_y = read_word(0x45)
    gyro_z = read_word(0x47)
    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z

# === Калибровка гироскопа ===
def calibrate_gyro(samples=500):
    print("Калибровка гироскопа...")
    gx_off, gy_off, gz_off = 0, 0, 0
    for _ in range(samples):
        _, _, _, gx, gy, gz = read_accel_gyro()
        gx_off += gx
        gy_off += gy
        gz_off += gz
        time.sleep(0.002)
    gx_off /= samples
    gy_off /= samples
    gz_off /= samples
    print(f"Смещения гироскопа: gx={gx_off:.2f}, gy={gy_off:.2f}, gz={gz_off:.2f}")
    return gx_off, gy_off, gz_off

# === Основная программа ===
def main():
    mpu_init()
    gx_off, gy_off, gz_off = calibrate_gyro()

    # Константы фильтра
    K = 0.98
    dt = 0.01
    angle_x = 0.0
    angle_y = 0.0
    prev_time = time.time()

    print("\nСчитывание данных... Нажми Ctrl+C для выхода.\n")

    while True:
        ax, ay, az, gx, gy, gz = read_accel_gyro()

        # Коррекция смещений
        gx -= gx_off
        gy -= gy_off
        gz -= gz_off

        # Расчёт углов из акселерометра
        accel_angle_x = math.degrees(math.atan2(ay, math.sqrt(ax**2 + az**2)))
        accel_angle_y = math.degrees(math.atan2(-ax, math.sqrt(ay**2 + az**2)))

        # Расчёт времени между итерациями
        now = time.time()
        dt = now - prev_time
        prev_time = now

        # Угловые скорости
        gyro_x_rate = gx / 131.0
        gyro_y_rate = gy / 131.0

        # Комплементарный фильтр
        angle_x = K * (angle_x + gyro_x_rate * dt) + (1 - K) * accel_angle_x
        angle_y = K * (angle_y + gyro_y_rate * dt) + (1 - K) * accel_angle_y

        print(f"Угол X={angle_x:6.2f}°,  Y={angle_y:6.2f}°", end="\r")
        time.sleep(0.01)

try:
    main()
except KeyboardInterrupt:
    print("\nЗавершено пользователем.")
