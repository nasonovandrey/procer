from subprocess import Popen
from select import select
import errno
import string
from sys import argv
import os
import pty
from datetime import datetime

from config import CONTROL_DIR


class Handler:
    def __init__(self, command, uid):
        self.command = command
        self.procdir = CONTROL_DIR+'/'+uid+'/'
        os.mkdir(self.procdir)
        self.profile = open(self.procdir+'profile', 'w+')
        
    def create_streams(self):
        master_stdout, self.slave_stdout = pty.openpty()
        out_file = open(self.procdir+'out.log', 'wb+')

        master_stderr, self.slave_stderr = pty.openpty()
        err_file = open(self.procdir+'err.log', 'wb+')

        self.streams = {master_stdout:out_file, master_stderr:err_file} 

    def run_command(self):
        self.profile.write(str(datetime.now())+'\n')
        self.profile.flush()

        try:
            proc = Popen(self.command, stdout=self.slave_stdout, stderr=self.slave_stderr)
        except e: raise
        finally:
            os.close(self.slave_stdout)
            os.close(self.slave_stderr)

        self.profile.write(str(proc.pid)+'\n')
        self.profile.flush()
        while self.streams:
            ready_fds, _, _ = select(list(self.streams.keys()), [], [])
            for fd in ready_fds:
                try:
                    output = os.read(fd, 1)
                    self.streams[fd].write(output)
                    self.streams[fd].flush()
                except OSError as e:
                    if e.errno != errno.EIO:
                        raise
                    output = ''
                if not output:
                    self.streams.pop(fd) 
        while True:
            if proc.poll() is not None:
                self.profile.write(str(datetime.now())+'\n')
                self.profile.flush()
                self.profile.write(str(proc.returncode)+'\n')
                self.profile.flush()
                self.profile.write('DONE\n')
                self.profile.close()
                return 0

if __name__ == '__main__':
    handler = Handler(argv[2:], argv[1])
    handler.create_streams()
    handler.run_command()
