# CircuitPython on Trinket M0 using Mu editor
# test program to read capacitive touch button and record on and off times in a series
# eventual plan is to distinguish long and short times and read Morse code

'''
# read-morse-code-from-hand-entry
Attempt to reliably read Morse code from hand entry

Planning to use capacitive touch input
Likely to be hard to read reliably
Want to be able to input a password, without a display
Only an LED for feedback, and do not feed back the password in case someone takes a video

Idea:
Read the input, store as a series of on-length,off-length pairs, until a long (1 sec?) off time
Calculate a histogram of on-length and separate dots and dashes
Calculate a histogram of off-length and separate dot/dash space from the spaces between letters
If all chars are valid, turn LED green, else red
'''

# imports
import board
import touchio
import time


# constants


# variables
touch1 = touchio.TouchIn(board.D1)
touch3 = touchio.TouchIn(board.D3)

# subroutines
def watchbutton(button1, button2):
    button_prev = 0
    button_times=[]
    button_times.append(time.monotonic())
    while True:
        button_new=button1.value
        if button_new != button_prev:
            button_times.append(time.monotonic())
            button_prev=button_new
        time.sleep(.01)
        if button2.value:
            return button_times

def showtimes(button_times):
    print("first ten cycles")
    prev=button_times[0]
    index=1
    for button_time in button_times[1:]:
        print(1-(index % 2),button_time - prev)
        prev=button_time
        index += 1
        if index > 30:
            return
    return

def histogram(button_times,start):
    a=[button_times[index] for index in range(start, len(button_times),2)]
    print(a)

# main
while True:
    button_times=watchbutton(touch1, touch3)
    showtimes(button_times)
    while touch3.value:
        time.sleep(.1)
        print(".", end="")
    print()