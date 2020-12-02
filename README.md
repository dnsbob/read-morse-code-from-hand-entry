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
