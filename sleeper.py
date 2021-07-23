from time import sleep
import sys

for i in range(int(sys.argv[1])):
    sleep(0.5)
    print(i)
raise Exception('This is just a drill')
