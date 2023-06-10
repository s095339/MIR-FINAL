# %%
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import logging
import math
import statistics
import sys
from scipy.io import wavfile
from pydub import AudioSegment

import matplotlib.pyplot as plt

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

#print("tensorflow: %s" % tf.__version__)
#print("librosa: %s" % librosa.__version__)



# %% resample the audio with 16kHz and ouput a wav file
def convert_audio_for_model(user_file, output_file='converted_audio_file.wav'):
  EXPECTED_SAMPLE_RATE = 16000
  audio = AudioSegment.from_file(user_file)
  audio = audio.set_frame_rate(EXPECTED_SAMPLE_RATE).set_channels(1)
  audio.export(output_file, format="wav")
  return output_file

# %% convert the output of model from 0~1 to frequency
def output2hz(pitch_output):
  # Constants taken from https://tfhub.dev/google/spice/2
  PT_OFFSET = 25.58
  PT_SLOPE = 63.07
  FMIN = 10.0;
  BINS_PER_OCTAVE = 12.0;
  cqt_bin = pitch_output * PT_SLOPE + PT_OFFSET;
  return FMIN * 2.0 ** (1.0 * cqt_bin / BINS_PER_OCTAVE)

# %% calculate the offset of human voice
def hz2offset(freq):
  A4 = 440
  C0 = A4 * pow(2, -4.75)
  # This measures the quantization error for a single note.
  if freq == 0:  # Rests always have zero error.
    return None
  # Quantized note.
  h = round(12 * math.log2(freq / C0))
  return 12 * math.log2(freq / C0) - h

# %% convert the frequency to pitch
def hz2pitch(freq, ideal_offset):
    A4 = 440
    C0 = A4 * pow(2, -4.75)
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    h = round(12 * math.log2(freq / C0) - ideal_offset)
    #h = round(12 * math.log2(freq / C0))
    octave = h // 12
    n = h % 12
    return note_names[n] + str(octave)

# %% The main function
# input: the path of audio
# output: a list of predicted pitches for each 32ms
def vocal_pitch_recognition(file_path):
    #EXPECTED_SAMPLE_RATE = 16000
    converted_audio_file = convert_audio_for_model(file_path)
    sample_rate, audio_samples = wavfile.read(converted_audio_file, 'rb')
    duration = len(audio_samples)/sample_rate
    print(f'Sample rate: {sample_rate} Hz')
    print(f'Total duration: {duration:.2f}s')
    print(f'Size of the input: {len(audio_samples)}')
    MAX_ABS_INT16 = 32768.0
    audio_samples = audio_samples / float(MAX_ABS_INT16)

    model = hub.load("https://tfhub.dev/google/spice/2")
    model_output = model.signatures["serving_default"](tf.constant(audio_samples, tf.float32))

    pitch_outputs = model_output["pitch"]
    uncertainty_outputs = model_output["uncertainty"]
    confidence_outputs = 1.0 - uncertainty_outputs
    confidence_outputs = list(confidence_outputs)
    pitch_outputs = [ float(x) for x in pitch_outputs]

    pitch_outputs_and_rests = [
    output2hz(p) if c >= 0.9 else 0
    for p, c in zip(pitch_outputs, confidence_outputs)
    ]

    plt.plot(pitch_outputs_and_rests)
    plt.show()
    offsets = [hz2offset(p) for p in pitch_outputs_and_rests if p != 0]
    ideal_offset = statistics.mean(offsets)
    pitches = [hz2pitch(p, ideal_offset) if p != 0 else 0 for p in pitch_outputs_and_rests]
    return pitches,pitch_outputs_and_rests