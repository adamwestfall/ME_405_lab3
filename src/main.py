"""!
@file main.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

    This file contains the code to succesfully run 2 motors with motor control 
    according to lab3 of ME-405. 
        * the motors run a step response and dump that data to the terminal in
            which it can be copied to a csv (this can be replaced by a uart or other connection 
            but is simple this way)
        * only the data from the step response is printed to the terminal once 
            the rest of the data from the run is not printed to the terminal

        

@author Adam Westfall
@author Jason Davis
@author Conor Fraser
@copyright                          Creative Commons CC BY: Please visit https://creativecommons.org/licenses/by/4.0/ to learn more
@date                               January 9, 2023
TODO: 
    * Test prevous functionality on boards
    * Implement motor control for one motor 
        * cotask.py should have timing at around 10ms
        * make sure run() method in controllor class only does one calc each time
        * Run the motor with a flywheel
            * print results and plot step response like before
            * find the slowest rate at which the controllers preformance is noticably worse
            * Record the slowest rate at which the performance is not significantly worse than when running the controller at a fast rate
            * choose a good run rate for the motor control task - it should be a bit faster than the slowest rate which works for a factor of safety
            * Save copies of the step response plots for the slowest rate at which the response is good and for a rate at which the response isn't as good.
    * make two tasks which run two motors under closed-loop control at the same time
        * write a test program which moves your motors simultaneously through different distances and holds them at the desired positions

"""

import gc
import pyb
import cotask
import task_share


def task1_fun(shares):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_share, my_queue = shares

    counter = 0
    while True:
        my_share.put(counter)
        my_queue.put(counter)
        counter += 1

        yield 0


def task2_fun(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    the_share, the_queue = shares

    while True:
        # Show everything currently in the queue and the value in the share
        print(f"Share: {the_share.get ()}, Queue: ", end='')
        while q0.any():
            print(f"{the_queue.get ()} ", end='')
        print('')

        yield 0

def our_task1_fun(Kp: float, position: int):
    """!
    Task that runs a motor driver and dumps the data to the terminal
    @param Kp a floating point value for the proportional coefficient
    @param position an integer value for the position the motor is to go to (can be -/+)
    """
    pass

def our_task2_fun(Kp: float, position: int):
    """!
    Task that runs another motor driver and dumps the data to the terminal 
    @param Kp a floating point value for the proportional coefficient
    @param position an integer value for the position the motor is to go to (can be -/+)
    """
    pass




# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    """
    TODO:
        * implement the two functions with cotsk.py shouldnt be any task_share stuff
        
    
    """
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=400,
                        profile=True, trace=False, shares=(share0, q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=1500,
                        profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')