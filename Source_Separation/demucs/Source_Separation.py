from .separate import separate
import librosa 
import os
def Source_Separation(filename):
    path = os.getcwd()
    background,vocals = separate(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", filename])
    
    vocals = vocals.numpy()
    vocals = vocals[0] if vocals.ndim > 1 else vocals
    
    drum = background[0]
    drum = drum[0] if drum.ndim > 1 else drum

    bass = background[1]
    bass = bass[0] if bass.ndim > 1 else bass

    other = background[2]
    other = other[0] if other.ndim > 1 else other
    
    drum = drum.numpy()
    bass = bass.numpy()
    other = other.numpy()
    
    vocals = vocals - drum - bass - other
    background = drum + bass + other
    return background,vocals


