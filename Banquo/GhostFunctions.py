import pigpio

M1pwm = 12   # RPi pin cotrolling PWM for Motor 1 (orange wire)
M2pwm = 18   # RPi pin cotrolling PWM for Motor 2 (yellow wire)
M3pwm = 13   # RPi pin cotrolling PWM for Motor 3 (green wire)
M4pwm = 19   # RPi pin cotrolling PWM for Motor 4 (blue wire)

def convert2pwm(command):
    c_factor = 100/100
    center = 170
    
    if command < 0:
        raw = abs(command)
        raw = round((raw * c_factor), 0)
        pwm = int(center - raw)
        if pwm < 0:
            pwm = 0
    elif command > 0:
        raw = abs(command)
        raw = round((raw * c_factor), 0)
        pwm = int(center + raw)
        if pwm > 255:
            pwm = 255
    else:
        pwm = center
    print(pwm)
    return pwm


def drive4motors(pi, pwm):
    pi.set_PWM_dutycycle(M1pwm, pwm)
    pi.set_PWM_dutycycle(M2pwm, pwm)
    pi.set_PWM_dutycycle(M3pwm, pwm)
    pi.set_PWM_dutycycle(M4pwm, pwm)
    return
