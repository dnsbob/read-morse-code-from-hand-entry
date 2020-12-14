# CircuitPython on Trinket M0 using Mu editor
'''
# threebuttonmorsecode
Read Morse code from hand entry with three buttons:
dot, dash, space
Which will be much easier than a single button and variable timing

Planning to use capacitive touch input
Want to be able to input a password, without a display
Only an LED for feedback, and do not feed back the password in case someone takes a video

Idea:
Read the input, store as a series of dots and dashes in a string, a list of strings separated by spaces
Then convert to characters
If all chars are valid, turn LED green, else red
'''

# imports
import board
import touchio
import time
import board
import adafruit_dotstar as dotstar

# constants
sleep=.01

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
dot[0]=(0,255,0) # green

# note that Morse code does not have separate uppercase and lowercase
asciinum2morse=[
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        # space, !, ", #, $, %, &, '
        "", "-.-.--", ".-..-.", "", "", "", "", ".----.",
        # ( ) * + , - . /
        "-.--.", "-.--.-", "", ".-.-.", "--..--", "-....-", ".-.-.-", "-..-.",
        # 0 1 2 3 4 5 6 7
        "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...",
        # 8 9 : ; < = > ?
        "---..", "----.", "---...", "-.-.-.", "", "-...-", "", "..--..",
        # @ A B C D E F G
        ".--.-.", ".-", "-...", "-.-.", "-..", ".", "..-.", "--.",
        # H I J K L M N O
        "....", "..", ".---", "-.-", ".-..", "--", "-.", "---",
        # P Q R S T U V W
        ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--",
        # X Y Z [ \ ] ^ _
        "-..-", "-.--", "--..", "", "", "", "", "..--.-",
        # ' a b c d e f g
        "", ".-", "-...", "-.-.", "-..", ".", "..-.", "--.",
        # h i j k l m n o
        "....", "..", ".---", "-.-", ".-..", "--", "-.", "---",
        # p q r s t u v w
        ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--",
        # x y z { | } ~ DEL
        "-..-", "-.--", "--..", "", "", "", "", ""
]
#for i in range(33,127):
#    print(i,chr(i),asciinum2morse[i])

# create reverse table
# Note that lowercase will overwrite uppercase, so output will be lowercase
morse2ascii={}
for i,v in enumerate(asciinum2morse):
    if v != "":
        morse2ascii[v]=i

'''
for i in range(33,127):
    morse=asciinum2morse[i]
    if morse != "":
        print(i,chr(i),morse,morse2ascii[morse])
    else:
        print(i,chr(i),"none")
'''

# variables
touch1 = touchio.TouchIn(board.D1)   # red, space
touch3 = touchio.TouchIn(board.D3)   # blue, dash
touch4 = touchio.TouchIn(board.D4)   # yellow, dot

# subroutines
def watchbuttons(buttonlist):
    '''record dots and dashes in a strings, list of strings separated by space button
    two consecutive space button ends the list and returns it
    pass in a list of buttons for dot, dash, and space
    '''
    buttonuse=['dot','dash','space']
    out=[]
    dotdashlist=[]  # more efficient to add to a list of characters and join at the end
    buttonprev={}
    run=1
    while run:
        for i,button in enumerate(buttonlist):
            buttonnew=button.value
            if buttonnew != buttonprev.get(i):
                #print(i,buttonuse[i],buttonnew)
                buttonprev[i]=buttonnew
                if buttonnew==True:
                    if i == 0:  # dot
                        dotdashlist.append(".")
                        print(".",end="")
                    elif i==1:  # dash
                        dotdashlist.append("-")
                        print("-",end="")
                    else:       # space
                        if dotdashlist:
                            dotdash="".join(dotdashlist)
                            out.append(dotdash)
                            dotdashlist=[]
                            char=morse2ascii.get(dotdash)
                            print('found:',dotdash, char)
                            dot[0] = (0,0,0) # off
                            time.sleep(.2)
                            if char:
                                dot[0]=(0,255,0) # green
                            else:
                                dot[0]=(255,0,0) # red
                        else:
                            run=0
                    while button.value:
                        time.sleep(sleep)   # wait for button to be released
        time.sleep(sleep)   # debounce
    return out


def morse2char(morse):
    outlist=[]
    for dotdash in morse:
        i=morse2ascii.get(dotdash)
        if i:
            outlist.append(chr(i))
        else:
            print("warning, not recognized:",dotdash)
    return "".join(outlist)


# main
while True:
    out=watchbuttons([touch4,touch3,touch1])
    print("out:",out)
    word=morse2char(out)
    print("word:",word)
