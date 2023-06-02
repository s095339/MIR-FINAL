from .separate import separate
import librosa 
import os
def Source_Separation(filename):
    path = os.getcwd()
    vocal,no_vocal = separate(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", filename])
    no_vocal = no_vocal.numpy()
    no_vocal = no_vocal[0] if no_vocal.ndim > 1 else no_vocal
    path = os.path.join(path, filename)
    y, sr = librosa.load(path,sr =44100)
    vocal = y - no_vocal
    return vocal,no_vocal


