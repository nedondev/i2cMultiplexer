import smbus
import math
import time
from datetime import datetime

# power management register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

base_x_accel= [] 
base_y_accel= []
base_z_accel= []
base_x_gyro = [] 
base_y_gyro = [] 
base_z_gyro = [] 

last_read_time = []
last_x_angle = []
last_y_angle = []
last_z_angle = []
last_gyro_x_angle = []
last_gyro_y_angle = []
last_gyro_z_angle = []

bus = []
started = []
address = 0

def read_byte(adr, i):
    return bus[i].read_byte_data(address, adr)

def read_word(adr, i):
    high = bus[i].read_byte_data(address, adr)
    low = bus[i].read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

#cause it max 16 bit data bit python is further more than that
def read_word_2c(adr, i):
    val = read_word(adr, i)
    if (val >= 0x8000):
        return - (0x10000 - val)
    else :
        return val

def dist(a,b):
    result = math.sqrt((a*a)+(b*b))
    if result != 0:
        return result
    return 0.001

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def set_last_read_angle_data(time, x, y, z, x_gyro, y_gyro, z_gyro, i):
    global last_read_time
    global last_x_angle 
    global last_y_angle 
    global last_z_angle 
    global last_gyro_x_angle
    global last_gyro_y_angle
    global last_gyro_z_angle

    last_read_time[i] = time
    last_x_angle[i] = x
    last_y_angle[i] = y
    last_z_angle[i] = z
    last_gyro_x_angle[i] = x_gyro
    last_gyro_y_angle[i]= y_gyro
    last_gyro_z_angle[i]= z_gyro

def calibrate_sensors(i):
    if started[i] == 0:
        return {"result":-5}
    global base_x_accel 
    global base_y_accel 
    global base_z_accel 
    global base_x_gyro  
    global base_y_gyro  
    global base_z_gyro  

    num_read = 20
    x_accel = 0
    y_accel = 0
    z_accel = 0
    x_gyro = 0
    y_gyro = 0
    z_gyro = 0

    print("Calibrating...")
    for count in range(0,num_read):
        x_gyro += read_word_2c(0x43, i)
        y_gyro += read_word_2c(0x45, i)
        z_gyro += read_word_2c(0x47, i)
        x_accel += read_word_2c(0x3b, i)
        y_accel += read_word_2c(0x3d, i)
        z_accel += read_word_2c(0x3f, i)
        time.sleep(0.1)

    base_x_accel[i] = x_accel/num_read
    base_y_accel[i] = y_accel/num_read 
    base_z_accel[i] = z_accel/num_read 
    base_x_gyro[i] = x_gyro/num_read 
    base_y_gyro[i] = y_gyro/num_read  
    base_z_gyro[i] = z_gyro/num_read  
    print("Done.")

def initial_sensor_module(i):
    global started
    global bus
    global address
    
    address = 0x68
    print("address: ", hex(address))
    #Register 0x75 (WHO_AM_I)
    print("WHO_AM_I: ", hex(read_byte(0x75, i)))
    #MPU6050 is in sleep mode so awake in first timeuse:
    bus[i].write_byte_data(address, power_mgmt_1, 0)
    
    started[i] = 1
    calibrate_sensors(i)
    set_last_read_angle_data(datetime.now(), 0, 0, 0, 0, 0, 0, i)

def initial_all_sensor_module():
    bus.append(smbus.SMBus(3))
    bus.append(smbus.SMBus(4))
    bus.append(smbus.SMBus(5))
    for i in range(3):
        #select communication channel
        base_x_accel.append(0)
        base_y_accel.append(0)
        base_z_accel.append(0)
        base_x_gyro.append(0)
        base_y_gyro.append(0)
        base_z_gyro.append(0)

        last_read_time.append(0)
        last_x_angle.append(0)
        last_y_angle.append(0)
        last_z_angle.append(0)
        last_gyro_x_angle.append(0)
        last_gyro_y_angle.append(0)
        last_gyro_z_angle.append(0)

        started.append(0)
        initial_sensor_module(i)

def read_filtered_out(i):
    if started[i] == 0:
        return {"result":-5}
    try:
        temp_out = read_word_2c(0x41, i)
    
        gyro_xout = read_word_2c(0x43, i)
        gyro_yout = read_word_2c(0x45, i)
        gyro_zout = read_word_2c(0x47, i)
        
        accel_xout = read_word_2c(0x3b, i)
        accel_yout = read_word_2c(0x3d, i)
        accel_zout = read_word_2c(0x3f, i)

        t_now = datetime.now()

        FS_SEL = 131
        gyro_xout = (gyro_xout - base_x_gyro[i])/FS_SEL
        gyro_yout = (gyro_yout - base_y_gyro[i])/FS_SEL
        gyro_zout = (gyro_zout - base_z_gyro[i])/FS_SEL
        
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0
        
        RADIANS_TO_DEGREES = 180/math.pi

        accel_angle_y = math.atan(-1*accel_xout/ dist(accel_xout,accel_zout))*RADIANS_TO_DEGREES
        accel_angle_x = math.atan(accel_yout/ dist(accel_yout,accel_zout))*RADIANS_TO_DEGREES
        accel_angle_z = 0

        # Compute the (filtered) gyro angles
        dt = (t_now - last_read_time[i]).microseconds/1000000
        gyro_angle_x = gyro_xout*dt + last_x_angle[i]
        gyro_angle_y = gyro_yout*dt + last_y_angle[i]
        gyro_angle_z = gyro_zout*dt + last_z_angle[i]

        # Compute the drifting gyro angles
        unfiltered_gyro_angle_x = gyro_xout*dt + last_gyro_x_angle[i]
        unfiltered_gyro_angle_y = gyro_yout*dt + last_gyro_y_angle[i]
        unfiltered_gyro_angle_z = gyro_zout*dt + last_gyro_z_angle[i]

        # Apply the complementary filter to figure out the change in angle
        # - choice of alpha is estimated now.
        # Alpha depends on the sampling rate...
        alpha = 0.96
        angle_x = alpha * gyro_angle_x + (1.0 - alpha)*accel_angle_x
        angle_y = alpha * gyro_angle_y + (1.0 - alpha)*accel_angle_y
        angle_z = gyro_angle_z # Accelerometer doesn't given z-angle

        # Update the saved data with the lastest values
        set_last_read_angle_data(t_now, angle_x, angle_y, angle_z,\
                gyro_angle_x, gyro_angle_y, gyro_angle_z, i)
        data = {
            "result": 0,
            "id": i,
            "delta_time":dt,
            "gyro_angle_x":gyro_angle_x,
            "gyro_angle_y":gyro_angle_y,
            "gyro_angle_z":gyro_angle_z,
            "accel_angle_x":accel_angle_x,
            "accel_angle_y":accel_angle_y,
            "accel_angle_z":accel_angle_z,
            "angle_x":angle_x,
            "angle_y":angle_y,
            "angle_z":angle_z
        }
        return data
    except IOError:
        KeyboardInterrupt('An error occured trying to read..(IOError)')
    except KeyboardInterrupt:
        raise KeyboardInterrupt('The operation have been cancel by keyboard.(KeyboardInterrupt)')

def read_all_filtered_out():
    data = []
    for i in range(3):
        data.append(read_filtered_out(i))
    return data

if __name__ == "__main__":
    bus.append(smbus.SMBus(3))
    bus.append(smbus.SMBus(4))
    bus.append(smbus.SMBus(5))
    for i in range(3):
        #select communication channel
        base_x_accel.append(0)
        base_y_accel.append(0)
        base_z_accel.append(0)
        base_x_gyro.append(0)
        base_y_gyro.append(0)
        base_z_gyro.append(0)

        last_read_time.append(0)
        last_x_angle.append(0)
        last_y_angle.append(0)
        last_z_angle.append(0)
        last_gyro_x_angle.append(0)
        last_gyro_y_angle.append(0)
        last_gyro_z_angle.append(0)

        started.append(0)
        initial_sensor_module(i)
    while(1):
        for i in range(3):
            print(read_filtered_out(i))

