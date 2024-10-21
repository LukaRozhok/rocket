from machine import Pin, I2C
import time

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)

# Device address and registers
address = 0x6B   # update with your device's I2C address
OUTX_L_XL = 0x28

def init_sensor():
    # CTRL1_XL: Accelerometer control register
    CTRL1_XL = 0x10
    # ODR_XL = 104Hz, FS_XL = 2g
    odr_fs = 0x50  # binary 0101 0000

    i2c.writeto_mem(address, CTRL1_XL, bytes([odr_fs]))

# Initialize the sensor
# Define I2C bus
init_sensor()

def read_acc():
    # Write the start register address
    i2c.writeto(address, bytes([OUTX_L_XL]))
    
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

# Example of reading accelerometer values
while True:
    acc = read_acc()
    print(f"Acceleration -> X: {acc['x']}, Y: {acc['y']}, Z: {acc['z']}")
    time.sleep(1)
