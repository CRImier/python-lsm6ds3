import smbus

class LSM6DS3(object):

    # Gyroscope registers
    OUTX_L_G=0x22
    OUTX_H_G=0x23
    OUTY_L_G=0x24
    OUTY_H_G=0x25
    OUTZ_L_G=0x26
    OUTZ_H_G=0x27

    # Accelerometer registers
    OUTX_L_XL=0x28
    OUTX_H_XL=0x29
    OUTY_L_XL=0x2A
    OUTY_H_XL=0x2B
    OUTZ_L_XL=0x2C
    OUTZ_H_XL=0x2D

    # Control registers
    CTRL1_XL=0x10
    CTRL2_G=0x11
    CTRL3_C=0x12
    CTRL4_C=0x13
    CTRL5_C=0x14
    CTRL6_C=0x15
    CTRL7_G=0x16
    CTRL8_XL=0x17
    CTRL9_XL=0x18
    CTRL10_C=0x19

    # Unused constants
    WHO_AM_I=0x0F
    SCALE_FOR_2G=0.0001
    SCALE_FOR_4G=0.0002
    SCALE_FOR_8G=0.0004
    SCALE_FOR_16G=0.0008
    DIV_2G=100
    DIV_4G=200
    DIV_8G=400
    DIV_16G=1200
    SCALE_FOR_250_DPS=0.000875
    SCALE_FOR_500_DPS=0.00175
    SCALE_FOR_2000_DPS=0.0070
    DIV_250_DPS=875
    DIV_500_DPS=1750
    DIV_2000_DPS=7000

    initial_reg_values = [0x70, 0x4c, 0x44, 0x0, 0x0,
                          0x0, 0x50, 0x0, 0x38, 0x38]
    initial_registers = ['CTRL1_XL', 'CTRL2_G', 'CTRL3_C', 'CTRL4_C', 'CTRL5_C',
                         'CTRL6_C', 'CTRL7_G', 'CTRL8_XL', 'CTRL9_XL', 'CTRL10_C']

    def __init__(self, bus=1, addr=0x6a):
        # Initializing the I2C bus object
        self.bus_num = bus
        self.bus = smbus.SMBus(self.bus_num)
        if isinstance(addr, basestring):
            addr = int(addr, 16)
        self.addr = addr

    def detect(self):
        assert(self.read_reg(self.WHO_AM_I) == 0x69), "Identification register value \
                                                       is wrong! Pass 'detect=False' \
                                                       to setup() to disable the check."

    def setup(self, detect=True):
        if detect:
            self.detect()
        # Safety check
        assert(len(self.initial_reg_values) == len(self.initial_registers)), \
                "Number of initial registers is not equal to number of initial \
                 register values. Set 'lsm.initial_registers' properly!"
        # Writing initial values into registers
        for i, reg_name in enumerate(self.initial_registers):
            self.write_reg(getattr(self, reg_name), self.initial_reg_values[i])
        return True

    def get_raw_gyro_values(self):
        gxh = self.read_reg(self.OUTX_H_G)
        gxl = self.read_reg(self.OUTX_L_G)
        gx = (gxh << 4) | (gxl >> 4)
        if (gxh & 0x80): gx |= 0xF000

        gyh = self.read_reg(self.OUTY_H_G)
        gyl = self.read_reg(self.OUTY_L_G)
        gy = (gyh << 4) | (gyl >> 4)
        if (gyh & 0x80): gy |= 0xF000

        gzh = self.read_reg(self.OUTZ_H_G)
        gzl = self.read_reg(self.OUTZ_L_G)
        gz = (gzh << 4) | (gzl >> 4)
        if (gzh & 0x80): gz |= 0xF000

        return gx, gy, gz

    def get_raw_accel_values(self):
        axh = self.read_reg(self.OUTX_H_XL)
        axl = self.read_reg(self.OUTX_L_XL)
        ax = (axh << 4) | (axl >> 4)
        if (axh & 0x80): ax |= 0xF000

        ayh = self.read_reg(self.OUTY_H_XL)
        ayl = self.read_reg(self.OUTY_L_XL)
        ay = (ayh <<4) | (ayl >> 4)
        if (ayh & 0x80): ay |= 0xF000

        azh = self.read_reg(self.OUTZ_H_XL)
        azl = self.read_reg(self.OUTZ_L_XL)
        az = (azh << 4) | (azl >> 4)
        if (azh & 0x80): az |= 0xF000

        return ax, ay, az

    def write_reg(self, reg, val):
        return self.bus.write_byte_data(self.addr, reg, val)

    def read_reg(self, reg):
        return self.bus.read_byte_data(self.addr, reg)

if __name__ == "__main__":
    from time import sleep
    lsm = LSM6DS3()
    lsm.setup()
    while True:
        ax, ay, az = lsm.get_raw_accel_values()
        print("Raw accel values: \t X {} \t Y {} \t Z {}".format(ax, ay, az))
        sleep(0.02)
    while True:
        gx, gy, gz = lsm.get_raw_gyro_values()
        print("Raw gyro values: \t X {} \t\t Y {} \t\t Z {}".format(gx, gy, gz))
        sleep(0.02)
