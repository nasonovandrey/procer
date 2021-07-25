from multiprocessing.connection import Client
from subprocess import Popen
from random import choice
from string import ascii_letters
from sys import argv


if __name__ == '__main__':
    command = argv[1]
    if command == '--start':
        process = Popen(['python', 'profiler.py'])
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
        uid = ''.join(choice(ascii_letters) for _ in range(8))
        address = ('localhost', 6000)
        conn = Client(address)
        conn.send(uid)
        process = Popen(['python', 'handler.py', uid]+argv[2:])
        