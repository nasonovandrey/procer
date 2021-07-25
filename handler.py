import subprocess
from select import select
import errno
import string
import sys
import os
import pty
from datetime import datetime


CONTROL_DIR = '/home/kieserel/.procer'


if __name__ == '__main__':

    uid = sys.argv[1]
    os.mkdir(CONTROL_DIR+'/'+uid)

    out_r, out_w = pty.openpty()
    err_r, err_w = pty.openpty()
    profile = open(CONTROL_DIR+'/'+uid+'/'+'profile', 'w+')

    profile.write(str(datetime.now())+'\n')
    profile.flush()


    proc = subprocess.Popen(sys.argv[2:], stdout=out_w, stderr=err_w)
    os.close(out_w)
    os.close(err_w)

    pid = proc.pid
    profile.write(str(pid)+'\n')
    profile.flush()

    outfile = open(CONTROL_DIR+'/'+uid+'/'+'outfile', 'wb+')
    errfile = open(CONTROL_DIR+'/'+uid+'/'+'errfile', 'wb+')

    streams = {out_r:outfile, err_r:errfile}

    while streams:
        ready_fds, _, _ = select(list(streams.keys()), [], [])
        for fd in ready_fds:
            try:
                output = os.read(fd, 1)
                streams[fd].write(output)
                streams[fd].flush()
            except OSError as e:
                if e.errno != errno.EIO:
                    raise
                output = ''
            if not output:
                streams.pop(fd)

        
    profile.write(str(datetime.now())+'\n')
    profile.write(str(proc.returncode)+'\n')
    profile.write('DONE\n')
    profile.close()
 
