import GhostFunctions as GF
import sys

while True:
    data = input("Enter speed value: ")
    
    if data == "no":
        sys.exit()
        
    data = int(data)
    
    pwm = GF.convert2pwm(data)

    print(pwm)
    print()
