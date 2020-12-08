# piano-video-to-midi
A Python program that scans piano videos (like from Synthesia) and converts them to MIDI.

# Usage
First you need to install the following software:

  * [ffmpeg](https://ffmpeg.org/)
  * [python3](https://www.python.org/) (obviously)

Then the following PIP packages:
  * ffmpeg-python
  * pillow
  * py_midicsv

After installing the dependencies you need to obtain a video. (possible with [youtube-dl](https://youtube-dl.org/))

Edit the config.py to include the parameters from your video, the times at which the playing starts and stops, tempo and the desired note velocity.

Then you'll need to edit the key mapping according to your video. Take a screengrab and use something like GIMP to get the screen coordinates of two keys on the far ends of the piano. Write down their common y-coordinate, and their x-coordinates. Then their pitches, using this helpful chart:

![piano pitch chart](https://www.researchgate.net/profile/Mickael_Tits/publication/283460243/figure/download/fig8/AS:614346480685058@1523483023512/88-notes-classical-keyboard-Note-names-and-MIDI-numbers.png)

Run the python script:

    python3 script.py

Enjoy your MIDI file!
