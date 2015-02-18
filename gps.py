import serial

ser = serial.Serial('/dev/ttyAMA0',4800)
while 1:
	print ser.readline()