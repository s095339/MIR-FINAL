import os
import argparse
import pyaudio
import wave
import soundfile as sf
import pygame
from pydub import AudioSegment

#-------------
from Source_Separation.separation import getSeparation
from Pitch_detection_model.SPICE import vocal_pitch_recognition
from lib.validate import validate
#-------------
DataBase_path = "./Database"

def arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-mode", help="i: import song \nr:record sining \nv:validate", type=str, default="r")
    parser.add_argument("-song_path", help="the .wav/.mp3 file of song to be imported", type=str)
    args = parser.parse_args()
    return args
def freq2file(path, freq_list):
    """
    Store the given freq_list into a txt file to the given path 
    """
    with open(path, mode='w') as F:
        for freq in freq_list:
            F.writelines(str(freq))
            F.writelines("\n")
    return 


def import_songs(args):
    """
    Source Separation model
    -------------------
    Separate the human voice and accompaniment from the given song file.
    And then apply the vocal pitch recognition to human voice to get a list of pitches every 0.1 sec.
    """

    #Source_Separation
    song_file = args.song_path.split("/")[-1]
    file_format = song_file[-4:]
    song_name = song_file.replace(file_format,"")
    print(f"Getting Separated source from path {song_file}")
    accompaniment,vocal, sr= getSeparation(args.song_path)

    #pitch recognition
    

    dir_path = os.path.join(DataBase_path, song_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    acc_file = os.path.join(dir_path,"accompaniment.wav")
    vocal_file = os.path.join(dir_path,"vocal.wav")
    sf.write(acc_file, accompaniment, sr)
    sf.write(vocal_file, vocal, sr)

    pitch_list, freq_list = vocal_pitch_recognition(vocal_file)
    #print(freq_list)
    #dump to .txt file
    freq_list_file = os.path.join(dir_path,"freq.txt")

    freq2file(freq_list_file, freq_list)

    
    return

def record(args):
    """
    Record your singing and apply the vocal pitch generation to generate a song list
    --------------------------
    
    "PyAudio" may be a useful library to  record microphone input
    
    """
    #Sample code-------------------------------
    # the parameter can be modified
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    song_list = os.listdir("./Database")
    print("Choose a song")
    for idx, song in enumerate(song_list):
        print(idx,":",song)
    song_idx = int(input("Enter a song id: "))
    song_name = song_list[song_idx]
    song_dir = os.path.join("./Database",song_list[song_idx])
    bgm = os.path.join(song_dir,"accompaniment.wav")

    

    music = AudioSegment.from_file(bgm)
    duration_in_seconds = len(music) / 1000
    print(duration_in_seconds)

    # Open the audio stream to record audio
    p = pyaudio.PyAudio()
    stream_input  = p.open(
        format = FORMAT,
        channels=CHANNELS,
        rate = RATE,
        input=True,
        frames_per_buffer=CHUNK
    )    

    # Turn on the audio stream to play music
    pygame.mixer.init()
    pygame.mixer.music.load(bgm)
    pygame.mixer.music.play()

    # record and write audio data
    print("start recording...")
    i=0
    k=0
    frames = []
    while pygame.mixer.music.get_busy():
        if i % int(RATE / CHUNK) == 0:
            data = stream_input.read(CHUNK)
            frames.append(data)
            print("--------------------------------------------------------------------")
            print(k)
            k=k+1
        
        i = i+1
    print("recording stopped")

    # stop recording
    stream_input.stop_stream()
    stream_input.close()
    p.terminate()

    # dump the data to a .wav file and save
    if not os.path.exists("./recorded"):
        os.mkdir("./recorded")
    recorded_dir_path = os.path.join("./recorded",song_name)

    if not os.path.exists(recorded_dir_path):
        os.mkdir(recorded_dir_path)
    recorded_song_path = os.path.join(recorded_dir_path, "output.wav")
    wf = wave.open(recorded_song_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Stop playing music
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    #convert recording to freq_list
    
    _,freq_list = vocal_pitch_recognition(recorded_song_path)
    recorded_freq_path = os.path.join(recorded_dir_path, "freq.txt")
    freq2file(recorded_freq_path,freq_list)
    #------------------------------------------
    #freq2file
    return recorded_freq_path, song_name

def scoring(args, recorded_freq_path, ref_song_name):
    import matplotlib.pyplot as plt
    ref_song_dir = os.path.join("./Database", ref_song_name)
    ref_freq_list = []
    with open(os.path.join(ref_song_dir, "freq.txt"),'r') as F:
        for line in F.readlines():
            ref_freq_list.append(float(line.replace("\n","")))
    
    freq_list_recorded = []
    with open(recorded_freq_path,'r') as F:
        for line in F.readlines():
            freq_list_recorded.append(float(line.replace("\n","")))

    plt.subplot(2,1,1)
    plt.plot(ref_freq_list)
    plt.title("ref song")
    plt.subplot(2,1,2)
    plt.plot(freq_list_recorded)
    plt.title("recorded song")
    plt.show()
    #print(ref_freq_list)

    print(f"score = {validate(ref_freq_list,freq_list_recorded)}")


    return
if __name__ == '__main__':
    args = arg()
    # print(args.m)
    print(args.song_path)
    if args.mode == 'r':
        freq_list, song_name= record(args)
        scoring(args, freq_list, song_name)
    elif args.mode == 'i':
        import_songs(args)
    elif args.mode == 'v':
        song_list = os.listdir("./Database")
        print("Choose a song")
        for idx, song in enumerate(song_list):
            print(idx,":",song)
        song_idx = int(input("Enter a song id: "))
        song_name = song_list[song_idx]
        recorded_freq_path = os.path.join("./recorded",song_name,"freq.txt")
        scoring(args,recorded_freq_path,song_name)