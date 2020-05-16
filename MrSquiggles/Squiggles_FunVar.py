#########################
#     MrSquiggles       #
#  Functions/Variables  #
#########################

import struct
import pigpio

# Sensor Variables
COMMAND = 0x80
ATIME = 0x01
ITIME = 0xFF
GAIN = 0x01
CONTROL = 0x0F
ENABLE = 0x00
ENABLE_AEN = 0x02
ENABLE_PON = 0x01

sensorList = [4, 8, 16 ,32]
colorRegisters = [0x16, 0x18, 0x1A, 0x14]


def getSensorData(pi, mux, sensor):
    """ Pulls sensor data from the registers on the chip.

        Returns a list ('data') with readings for r/g/b/c on all
                three sensors.

        data[0] = r1    data[4] = r2    data[8] = r3    data[12] = r4
        data[1] = g1    data[5] = g2    data[9] = g3    data[13] = g4
        data[2] = b1    data[6] = b2    data[10] = b3   data[14] = b4
        data[3] = c1    data[7] = c2    data[11] = c3   data[15] = c4
        """
    data = []
    for s in sensorList:
        pi.i2c_write_byte(mux, s)
        for reg in colorRegisters:
            (c, d) = pi.i2c_read_i2c_block_data(sensor,
                                                (COMMAND | reg), 2)
            neat = struct.unpack('H'*1, d)
            data.append(neat[0])
    return data
