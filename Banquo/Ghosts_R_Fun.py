from time import sleep

from cardinalDirections import *
import Ghost_Class as GC

Banquo = GC.Ghost('10.3.141.67')

#Banquo.drive(320, 50)
Banquo.spin(CCW,50)

sleep(1)
Banquo.stop()

Banquo.closeSerial()
print('All done!')
