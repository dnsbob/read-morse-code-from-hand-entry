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
div=.02
maxcount=100

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
            button_times.append(time.monotonic())
            return button_times

def get_up_down_times(button_times):
    up_down_times=[]
    prev=button_times[0]
    for mytime in button_times[1:]:
        diff=mytime-prev
        up_down_times.append(diff)
        prev=mytime
    return up_down_times

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

def histogram(up_down_times,start):
    a=[up_down_times[index] for index in range(start,len(up_down_times),2)]
    # [button_times[index] - button_times[index-1] for index in range(start, len(button_times),2)]
    b=a.copy()
    print(a)
    ascii_barchart(a,.01,"*")
    b.sort()
    print(b)
    avg=sum(a)/len(a)
    for myround in [1, 2]:
        print("average",avg)
        ascii_barchart(avg,div,"=")
        probhi=[x for x in a if x > avg]
        avghi=sum(probhi)/len(probhi)
        print("avghi", avghi)
        ascii_barchart(avghi,div,">")
        problo=[x for x in a if x <= avg]
        avglo=sum(problo)/len(problo)
        print("avglo",avglo)
        ascii_barchart(avglo,div,"<")
        avg=(avglo+avghi)/2
    print("avg",avg)
    ascii_barchart(avg,div,"-")
    return avg

def ascii_barchart(data,div,char):
    if type(data) is type([]):
        mydata=data
    else:
        mydata=[data]
    for x in mydata:
        print(x,"".join([char for x in range(int(x/div))]))

def ascii_barchart2(data,div,char1,char2):
    for i,v in enumerate(data):
        up=i%2
        if up:
            mychar=char2
        else:
            mychar=char1
        count=int(v/div)
        if count>maxcount:
            count=maxcount
        bar=""
        for x in range(count):
            bar += mychar
        print('{0:} {1:.2f} {2:}'.format(i%2,v,bar))

def read_dot_dash_space(button_times,avgoff,avgon):
    '''read times, convert to dot, dash, and spaces between words based on avgoff and avgon times,
    return list of dots and dashes like [".-","--.","..-."] which is chars "ngf" '''
    # input starts with keypress time, ends with a release
    dotdash=[]
    signal=1
    dots=""
    for x in range(1,len(button_times)-1,2):
        on=button_times[x]-button_times[x-1]
        if on < avgon:
            dots += "."
            print("dot",on)
        else:
            dots += "-"
            print("dash",on)
        off=button_times[x+1]-button_times[x]
        if off > avgoff:
            # start new char
            print("char was",dots,off)
            dotdash.append(dots)
            dots=""
    if dots:
        dotdash.append(dots)
        dotdash.append(dots)
    return dotdash

# main
while True:
    button_times=watchbutton(touch1, touch3)
    print("#times",len(button_times))
    up_down_times=get_up_down_times(button_times)
    print("#updown",len(up_down_times))
    showtimes(button_times)
    while touch3.value:
        time.sleep(.1)
        print(".", end="")
    print()
    ascii_barchart2(up_down_times,div,".","*")
    print("sorted off")
    avgoff=histogram(up_down_times,2)
    print("sorted on")
    avgon=histogram(up_down_times,1)
    dotdash=read_dot_dash_space(button_times,avgoff,avgon)
    print(dotdash)
    print("end")
