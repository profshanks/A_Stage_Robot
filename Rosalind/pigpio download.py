try:
    import pigpio

except:
    import pip
    pip.main(['install', 'pigpio'])

print ("Hello World")
