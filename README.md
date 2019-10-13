# i2cMultiplexer
TCA9548A is I2C Multiplexer Module.This repository try to use it for communicate with multiple I2C module.

3D box control for visualize:
![alt text](https://raw.githubusercontent.com/nedondev/i2cMultiplexer/master/image/Multiplexer_3dbox.png)

Multiplexer connect with Raspberry Pi 3 Model B+ and MPU6050:
![alt text](https://raw.githubusercontent.com/nedondev/i2cMultiplexer/master/image/IMU_Multiplexer_diagram.png)

find i2c bus:
```bash
$ i2cdetect -l
i2c-3	i2c       	i2c-1-mux (chan_id 0)           	I2C adapter
i2c-1	i2c       	bcm2835 I2C adapter             	I2C adapter
i2c-8	i2c       	i2c-1-mux (chan_id 5)           	I2C adapter
i2c-6	i2c       	i2c-1-mux (chan_id 3)           	I2C adapter
i2c-4	i2c       	i2c-1-mux (chan_id 1)           	I2C adapter
i2c-9	i2c       	i2c-1-mux (chan_id 6)           	I2C adapter
i2c-10	i2c       	i2c-1-mux (chan_id 7)           	I2C adapter
i2c-7	i2c       	i2c-1-mux (chan_id 4)           	I2C adapter
i2c-5	i2c       	i2c-1-mux (chan_id 2)           	I2C adapter
```

smbus reference:
IBEX UK, Limited."Using the I2C Interface"
Available: https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2

tca9548a reference:
Ashish Adhikari. "TCA9548A I2C MULTIPLEXER MODULE - WITH ARDUINO AND NODEMCU"
Available: https://diyfactory007.blogspot.com/2018/11/tca9548a-i2c-multiplexer-module-with.html
Luis Valencia. "How to read from multiplexer with python I2C TCA9548A"
Available: https://stackoverflow.com/questions/41335921/how-to-read-from-multiplexer-with-python-i2c-tca9548a
Texas Instruments, Inc."TCA9548A Low-Voltage 8-Channel I2C Switch with Reset datasheet (Rev. F)"
Available: https://www.ti.com/lit/ds/symlink/tca9548a.pdf
GeertVc."Support for I2c mux 9548 is in now?"
Available: https://www.raspberrypi.org/forums/viewtopic.php?t=243321
