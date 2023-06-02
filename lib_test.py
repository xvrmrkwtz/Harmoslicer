import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy
import sys
from pythonosc.udp_client import SimpleUDPClient

np.set_printoptions(threshold=sys.maxsize)

def load(filename):
    y, sr = librosa.load(filename, sr = 44100, duration = None)
    y = librosa.to_mono(y)

    return y, sr

def create_chroma(y, sr):
    chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)

    return chroma_cens

def del_quiet(y, chroma_cens):
    rms = librosa.feature.rms(y=y)
    rms = rms.flatten()
    too_quiet = []
    for i in range(rms.shape[0]):
        if rms[i] < .0035:
            too_quiet.append(i)
    # rms = np.delete(rms, too_quiet)
    # plt.plot(rms)
    # plt.show()
    chroma_cens = np.delete(chroma_cens, too_quiet, axis = 1)

    return chroma_cens

def display_chroma(chroma_cens):
    img = librosa.display.specshow(chroma_cens, y_axis='chroma', x_axis='time')
    plt.show()

def smooth_chroma(chroma_cens):
    smooth_dist = []
    for i in range(0, chroma_cens.shape[1], 10):
        if i+20 > chroma_cens.shape[1]:
            break
        dist = np.linalg.norm((chroma_cens[:,i:i+10] - chroma_cens[:, i+10:i+20]))
        smooth_dist.append(dist)
    
    return smooth_dist

def find_changes(smooth_dist, disc = .33):
    changes = 0
    frames = []
    for i in range(len(smooth_dist)):
        if i+1 == len(smooth_dist):
            break
        if (smooth_dist[i+1] - smooth_dist[i]) > disc:
            frames.append(i)
            changes += 1
    timestamps = librosa.frames_to_time(frames, sr = 44100)

    return timestamps

def udp_send(port, message):
    ip = "127.0.0.1"
    client = SimpleUDPClient(ip, port)
    client.send_message("set", message)

def write_to_file(timestamps):
    outstring = ""
    # for i in range(len(timestamps)):
    #     outstring += str(i) + ", " + str(timestamps[i]) + ";\n"
    for i in range(len(timestamps)):
        outstring += str(timestamps[i]) + "\n"
    print(outstring)
    with open('out.txt', 'w') as f:
        f.write(outstring)

def read_threshold():
    with open("threshold.txt", "r") as f:
        SMRF1 = f.readlines()
    return SMRF1

# fig, axs = plt.subplots(2, 2)

# axs[0, 0].plot(chroma_cens[0, :])
# axs[0, 1].plot(smooth_dist)
# plt.show()

# print(smooth_dist)
# print(max(smooth_dist))

def main():
    y, sr = load('test.wav')
    chroma = create_chroma(y, sr)
    chroma = del_quiet(y, chroma)
    chroma = smooth_chroma(chroma)
    timestamps = find_changes(chroma)
    # print(timestamps)
    udp_send(7000, timestamps)
    open("threshold.txt", "w").close()
    initial = read_threshold()
    while True:
        current = read_threshold()
        if initial != current:
            for line in current:
                
                timestamps = find_changes(chroma, disc = float(line))
                print(timestamps)
                if len(timestamps) == 0:
                    print("Threshold value too high")
                    continue
                elif timestamps[0] == 0:
                    timestamps = timestamps[1:]
                udp_send(7000, timestamps)
                open("threshold.txt", "w").close()
            initial = current


if __name__ == '__main__':
    main()