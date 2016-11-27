Phase 2 testing
---------------
The file phase2.in contains the simulator commands being tested.

Usage (just type the Linux commands on the > lines):

    > cp -r ~sasaki/Phase2 ~
           # To copy the phase 2 directory to your home
    > cd ~/Phase2
    > ln -s your_executable FP_Phase2
            # To link your executable to the Phase 2 directory
    > script test.out
    Script started, file is test.out  <- message from script command

Now you have a choice -- if you want to enter the simulator
commands yourself, use

    > ./FP_Phase2 basic.hex

If you want the simulator to read in the commands from
phase2.in, use

    > /FP_Phase2 basic.hex < phase2.in

In any case, once you quit the simulator, use exit to stop the
saving of output into test.out.

    > exit
    Script done, file is test.out  <- message from script command

