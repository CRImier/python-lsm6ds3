### LSM6DS3 Python library

Based on code from Roberts Gotlaufs

```python
from lsm6ds3 import LSM6DS3

lsm = LSM6DS3()
lsm.setup()

gx, gy, gz = lsm.get_raw_gyro_values()
print("Raw gyro values: X \t {} \t Y {} \t Z {}".format(gx, gy, gz))

ax, ay, az = lsm.get_raw_accel_values()
print("Raw accel values: X \t {} \t Y {} \t Z {}".format(ax, ay, az))
```

#### Changing the initial values for control registers 

```python
>>> lsm = LSM6DS3()
>>> print(lsm.initial_registers)
['CTRL1_XL', 'CTRL2_G', 'CTRL3_C', 'CTRL4_C', 'CTRL5_C', 'CTRL6_C', 'CTRL7_G', 'CTRL8_XL', 'CTRL9_XL', 'CTRL10_C']
>>> # Changing value for control register CTRL5_C, 5th in the list
>>> lsm.initial_registers[5] = 0x36
>>> # Then, call `setup()` to populate the registers with values
>>> lsm.setup()
```

#### Writing to arbitrary registers:

```python
lsm = LSM6DS3()
lsm.setup() # In this case, it's not always necessary:
            # All `setup()` does is set up the initial registers,
            # so if you're setting all of them yourself,
            # you won't have to call it.

lsm.write_reg(lsm.CTRL1_XL, 0x1)
lsm.write_reg(0x12, 0x45)
```

#### Reading from arbitrary registers:

```python
lsm = LSM6DS3()
lsm.setup()

lsm.write_reg(lsm.CTRL1_XL, 0x1)
lsm.write_reg(0x12, 0x45)
```

#### Using another I2C address / bus number

Default bus number: 1

```python
lsm = LSM6DS3(addr = 0x67)
```

```python
lsm = LSM6DS3(addr = '0x67')
```

```python
lsm = LSM6DS3(bus = 3)
```

