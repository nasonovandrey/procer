# Disclaimer
This is still a work on progress.
This program may be hard on your harddrive as it is writing logs to files in realtime.

# Description
Simple utility to use instead of detaching with tmux/screen.

# Installation
Do git clone into home directory, then puth $HOME/procer into your path.

# Usage
Start procer:
procer --start

Look at the list of started processes:
procer --show

Start new process:
procer --run your_command_goes_here

Clear .procer directory and stop profiler demon (this program does NOT terminate all the started processes, you will have to it manually):
procer --clear

To look at the logs you would have to get the uuid of your process (procer --show) and then go to the directory ~/.procer/uuid_of_your_process.
