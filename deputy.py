import subprocess
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
    outfile = open(CONTROL_DIR+'/'+uid+'/'+'outfile', 'wb+')
    errfile = open(CONTROL_DIR+'/'+uid+'/'+'errfile', 'wb+')
    profile = open(CONTROL_DIR+'/'+uid+'/'+'profile', 'w+')

    profile.write(str(datetime.now())+'\n')
    profile.flush()

    proc = subprocess.Popen(sys.argv[2:], stdout=out_w, stderr=err_w)
    os.close(out_w)
    os.close(err_w)

    pid = proc.pid
    profile.write(str(pid)+'\n')
    profile.flush()

    while proc.poll() is None:
        outline = os.read(out_r, 1000)
        errline = os.read(err_r, 1000)
        outfile.write(outline)
        outfile.flush()
        errfile.write(errline)
        errfile.flush()
        
    profile.write(str(datetime.now())+'\n')
    profile.write(str(proc.returncode)+'\n')
    profile.write('DONE\n')
    profile.close()
    
    
