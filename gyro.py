from machine import Pin, I2C
import time

# Define I2C bus
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)

# Device address and registers
address = 0x6B  # update with your device's I2C address
OUTX_L_G = 0x22  # Gyroscope register for X low byte

def init_gyro():
    # CTRL2_G: Gyroscope control register
    CTRL2_G = 0x11
    # ODR_G = 104Hz, FS_G = 2000dps
    odr_fs = 0x50  # binary 0101 0000

    i2c.writeto_mem(address, CTRL2_G, bytes([odr_fs]))

# Initialize the gyroscope
init_gyro()

def read_gyro():
    # Write the start register address
    i2c.writeto(address, bytes([OUTX_L_G]))
    
    # Read 6 bytes of data
    data = i2c.readfrom(address, 6)
    
    # Combine the high and low bytes
    x = (data[1] << 8) | data[0]
    y = (data[3] << 8) | data[2]
    z = (data[5] << 8) | data[4]
    
    # Convert to signed 16-bit values
    if x > 32767: x -= 65536
    if y > 32767: y -= 65536
    if z > 32767: z -= 65536
    
    return {'x': x, 'y': y, 'z': z}

# Example of reading gyroscope values
while True:
    gyro = read_gyro()
    print(f"Gyroscope -> X: {gyro['x']}, Y: {gyro['y']}, Z: {gyro['z']}")
    time.sleep(1)
