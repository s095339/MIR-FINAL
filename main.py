import os
import argparse
import pyaudio
import wave
import soundfile as sf
#-------------
from Source_Separation.separation import getSeparation
from Pitch_detection_model.vocal_pitch_recognition import vocal_pitch_recognition
#-------------
DataBase_path = "./Database"

def arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-mode", help="i: import song \nr:record sining", type=str, default="r")
    parser.add_argument("-song_path", help="the .wav/.mp3 file of song to be imported", type=str)
    args = parser.parse_args()
    return args

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
    vocal, accompaniment ,sr= getSeparation(args.song_path)

    #vocal pitch recognition
    #pitch_list = vocal_pitch_recognition(vocal)
    

    dir_path = os.path.join(DataBase_path, song_name)
    os.mkdir(dir_path)
    acc_file = os.path.join(dir_path,"accompaniment.wav")
    vocal_file = os.path.join(dir_path,"vocals.wav")
    sf.write(acc_file, accompaniment, sr)
    sf.write(vocal_file, vocal, sr)

    #TODO: ------------------------------------------------------
    """
    save the original .wav file,accompaniment and vocal separated 
    from the file and pitch_list(e.g. in txt form) to the Database
    """


    #-------------------------------------------------------------
    return

def validate(args):
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

    p = pyaudio.PyAudio()
    stream = p.open(
        format = FORMAT,
        channels=CHANNELS,
        rate = RATE,
        input=True,
        frames_per_buffer=CHUNK
    )    

    print("start recording...")
    # record 3 sec
    frames = []
    seconds = 3
    for i in range(0, int(RATE/CHUNK*seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("recording stopped")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # dump the data to a .wav file and save
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    #------------------------------------------
    return


if __name__ == '__main__':
    args = arg()
    #print(args.m)
    print(args.song_path)
    if args.mode == 'r':
        validate(args)
    elif args.mode == 'i':
        import_songs(args)
