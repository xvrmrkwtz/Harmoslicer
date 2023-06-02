# Harmoslicer
The goal of this project was to create a prototype for a virtual instrument that can recognize when chords start and stop in a short sample of audio and can set timestamps for user playback. To accomplish this I used a combination of Python and Max MSP. I collaborated extensively with Professor José Martinez to write the Max Msp portion of this project.

I wrote a python script named lib_test.py that uses the Librosa Library to detect possible timestamps where chords are beginning. It does this by generating a smoothed chromagram of the audio sample which provides the best possible audio feature extraction for this task. The difference between each frame of audio is compared to find the most different frames, which I considered to be the points at which the chords changed. These timestamps are then outputted to Max.

Professor Martinez and I then collaboratively wrote a Max Msp patch that acts as a front end graphical interface that receives the timestamps from Python, slices the sample, and allows the user to play the individual slices. 

There is no native way for Python and Max to communicate so I needed to devise a system for the two to do so. To send the timestamps to Max, I used Open Sound Control or OSC to send UDP messages from Python to Max. To send changes in threshold values from Max back to Python, I had Max write to text file which Python is always reading.

This project acts as a proof of concept more than anything as it requires careful communication between both Python and Max. I plan on building and improving upon this concept by combining both parts into a single application written in C++ using the JUCE Framework.
