import mpu6050
import time
import sys

try:
    # Create a new Mpu6050 object
    mpu6050 = mpu6050.mpu6050(0x68)
    print("MPU6050 initialized successfully")
except Exception as e:
    print(f"Error initializing MPU6050: {e}")
    sys.exit(1)

def read_sensor_data():
    try:
        # Read the accelerometer values
        accelerometer_data = mpu6050.get_accel_data()
        
        # Read the gyroscope values
        gyroscope_data = mpu6050.get_gyro_data()
        
        # Read temp
        temperature = mpu6050.get_temp()
        
        return accelerometer_data, gyroscope_data, temperature
        
    except OSError as e:
        print(f"I2C communication error: {e}")
        return None, None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None, None

# Main loop
while True:
    try:
        # Read the sensor data
        accelerometer_data, gyroscope_data, temperature = read_sensor_data()
        
        if accelerometer_data is not None:
            # Print the sensor data
            print("Accelerometer data:", accelerometer_data)
            print("Gyroscope data:", gyroscope_data)
            print("Temp:", temperature)
            print("-" * 40)
        else:
            print("Failed to read sensor data")
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        break
    except Exception as e:
        print(f"Error in main loop: {e}")
        
    # Wait for 1 second
    time.sleep(1)