from subprocess import Popen, PIPE
from multiprocessing.connection import Client
import psutil
import sys
import os
import random
import string


CONTROL_DIR = '/home/kieserel/.procer'


if __name__ == '__main__':
    command = sys.argv[1]
    if command == '--start':
        process = Popen(['python', 'warden.py'])
    elif command == '--show':
        address = ('localhost', 6000)
        conn = Client(address)
        conn.send('show')
        msg = conn.recv()
        print(msg)
        conn.close()
    elif command == '--stop':
        address = ('localhost', 6000)
        conn = Client(address)
        conn.send('stop')
        conn.close()
    elif command == '--run':
        uid = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        address = ('localhost', 6000)
        conn = Client(address)
        conn.send(uid)
        process = Popen(['python', 'deputy.py', uid]+sys.argv[2:])
        
