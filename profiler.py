from multiprocessing.connection import Listener
from tabulate import tabulate
import argparse


CONTROL_DIR='/home/kieserel/.procer/'


class Warden:

    def __init__(self, port):
        self.listener = Listener(('localhost', port))
        self.proc_list = []
        self.headers = ['uid', 'start_time', 'pid', 'end_time', 'return_code', 'status']
    
    def __call__(self):
        while True:
            conn = self.listener.accept()
            msg = conn.recv()
            if msg == 'show':
                if len(self.proc_list)==0:
                    conn.send('list of processes is empty')
                else:
                    profiles = []
                    for uid in self.proc_list:
                        file = open(CONTROL_DIR+uid+'/profile')
                        lines = []
                        for line in file:
                            lines.append(line)
                        profiles.append([uid]+lines)
                    msg = tabulate(profiles, self.headers)
                    conn.send(msg)
            elif msg == 'stop':
                conn.close()
                exit()
            else:
                self.proc_list.append(msg)
            


if __name__ == '__main__':
    warden = Warden(6000)
    warden()
