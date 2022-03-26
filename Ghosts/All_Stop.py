# Just stops the motors

from time import sleep

from cardinalDirections import *
import Ghost_Class as GC

Banquo = GC.Ghost('10.3.141.67')

Banquo.stop()

Banquo.closeSerial()
print('All done!')
