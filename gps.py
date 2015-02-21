import sys
import serial
<<<<<<< HEAD
=======
import sys
>>>>>>> d689cc68767b41c6f0b71431c2044eb26b56b42b
import datetime

start_time = datetime.datetime.now()
print start_time
f = open('gps_log.txt','w')
ser = serial.Serial('/dev/ttyAMA0',4800)
while 1:
<<<<<<< HEAD
        process_time = datetime.datetime.now()
        dt =  process_time - start_time
        result = dt.seconds
	if result >= 10:
	        sys.exit()
        else:
                print ser.readline()
                f.write(ser.readline())


=======
	print ser.readline()
>>>>>>> d689cc68767b41c6f0b71431c2044eb26b56b42b
