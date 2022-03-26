from time import sleep

from cardinalDirections import *
import Ghost_Class as GC

Banquo = GC.Ghost('10.3.141.67')

sp = 30
t = 4

Banquo.drive(NE, sp)
sleep(t)
Banquo.drive(S, sp)
sleep(t)
Banquo.drive(SW, sp)
sleep(t)
Banquo.drive(N, sp)
sleep(t)

'''
while sp <=100:
    print('Speed is ' + str(sp))
    Banquo.drive(N, sp)
    sleep(t)
    Banquo.drive(E, sp)
    sleep(t)
    Banquo.drive(S, sp)
    sleep(t)
    Banquo.drive(W, sp)
    sleep(t)

    sp += 10
    
Banquo.stop()
sleep(3)

sp = 1
while sp <= 100:
    Banquo.spin(CCW, sp)
    sleep(.3)
    sp += 1

while sp > 0:
    Banquo.spin(CW, sp)
    sleep(.3)
    sp -= 1
'''

Banquo.stop()

Banquo.closeSerial()
print('All done!')
