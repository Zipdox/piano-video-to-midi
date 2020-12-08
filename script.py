import ffmpeg
from PIL import Image
import csv
from config import *


keys = []
leftToRight = rightkeyX - leftkeyX
keyDistance = leftToRight/(rightkeyPitch-leftkeyPitch)
for i in range(leftkeyPitch, rightkeyPitch+1):
    keyX = int((i-leftkeyPitch)*keyDistance+leftkeyX)
    keys.append({'pos': (keyX, keysY), 'pitch': i, 'state': 'off', 'channel': 0})


keycolors = (
    (255, 250, 214, 'off'), # white key off
    (14, 14, 14, 'off'), # black key off
    (153, 255, 0, 'on', 'green'), # white key on green
    (125, 174, 236, 'on', 'blue'), # white key on blue
    (90, 198, 0, 'on', 'green'), # black key on green
    (49, 114, 244, 'on', 'blue') # black key on blue
)
def nearest_colour( subjects, query ):
    return min( subjects, key = lambda subject: sum( (s - q) ** 2 for s, q in zip( subject, query ) ) )


process1 = (
    ffmpeg
    .input(filename)
    .output('pipe:', format='rawvideo', pix_fmt='rgb24', r=60, vsync=1, loglevel='panic')
    .run_async(pipe_stdout=True)
)


bps = bpm/60
mspqn = 1000000/bps
ccpqn = 960

midimessages = []

midimessages.append([0,0,'Header',1,2,ccpqn])
midimessages.append([1,0,'Start_track'])
midimessages.append([1,0,'Tempo',int(mspqn)])
midimessages.append([1,0,'End_track'])
midimessages.append([2,0,'Start_track'])

framenum = 0
while True:
    in_bytes = process1.stdout.read(width * height * 3)
    time = framenum/framerate
    relativetime = time-starttime

    if framenum/framerate < starttime:
        framenum+=1
        continue

    if not in_bytes or (time >= endtime and endtime != 0):
        break

    frame = Image.frombytes("RGB", (1920, 1080), in_bytes, 'raw')
    for key in keys:
        pixel = frame.getpixel(key['pos'])
        match_key = nearest_colour(keycolors, pixel)
        keystate = match_key[3]

        if keystate == 'on':
            keycolor = match_key[4]
            if keycolor == 'green':
                key['channel'] = 0
            if keycolor == 'blue':
                key['channel'] = 1

        if keystate != key['state']:
            key['state'] = keystate
            if keystate == 'on':
                midimessages.append([2,int(relativetime*bps*ccpqn),'Note_on_c',key['channel'],key['pitch'],velocity])
            elif keystate == 'off':
                midimessages.append([2,int(relativetime*bps*ccpqn),'Note_off_c',key['channel'],key['pitch'],velocity])
            print(f"{relativetime:.2f} {key['pitch']} {key['state']}")

    framenum+=1

midimessages.append([2,int(relativetime*bps*ccpqn),'End_track'])
midimessages.append([0,0,'End_of_file'])

csvfile = open('midi.csv', 'w')
csvwriter = csv.writer(csvfile)
csvwriter.writerows(midimessages)
csvfile.close()
