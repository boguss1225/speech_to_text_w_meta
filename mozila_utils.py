
import argparse
import numpy as np
import shlex
import subprocess
import sys
import wave
import json
import os

from deepspeech import Model, version
from timeit import default_timer as timer
from utils import *

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path), desired_sample_rate)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))

    return desired_sample_rate, np.frombuffer(output, np.int16)

def metadata_to_string(metadata):
    return ''.join(token.text for token in metadata.tokens)

def words_from_candidate_transcript(metadata):
    word = ""
    word_list = []
    word_start_time = 0
    # Loop through each character
    for i, token in enumerate(metadata.tokens):
        # Append character to word if it's not a space
        if token.text != " ":
            if len(word) == 0:
                # Log the start time of the new word
                word_start_time = token.start_time

            word = word + token.text
        # Word boundary is either a space or the last character in the array
        if token.text == " " or i == len(metadata.tokens) - 1:
            word_duration = token.start_time - word_start_time

            if word_duration < 0:
                word_duration = 0

            each_word = dict()
            each_word["word"] = word
            each_word["start_time"] = round(word_start_time, 4)
            each_word["duration"] = round(word_duration, 4)

            word_list.append(each_word)
            # Reset
            word = ""
            word_start_time = 0

    return word_list

def metadata_json_output(metadata):
    json_result = dict()
    json_result["transcripts"] = [{
        "confidence": transcript.confidence,
        "words": words_from_candidate_transcript(transcript),
    } for transcript in metadata.transcripts]
    return json.dumps(json_result, indent=2)

# class VersionAction(argparse.Action):
#     def __init__(self, *args, **kwargs):
#         super(VersionAction, self).__init__(nargs=0, *args, **kwargs)

#     def __call__(self, *args, **kwargs):
#         print('DeepSpeech ', version())
#         exit(0)

def deepspeech_batch_stt(model, filename: str) -> str:
    buffer, rate = read_wav_file(filename)
    foo, buffer = convert_samplerate(filename, model.sampleRate())
    data16 = np.frombuffer(buffer, dtype=np.int16)

    return model.sttWithMetadata(data16)

def extract_from_json_deepspeech(JSON_DATA):
    response = json.loads(JSON_DATA)
    transcript_display_list=[]
    confidence_list=[]
    words_timestamp_list=[]
    confidence_list.append(response['transcripts'][0]['confidence'])
    transcript_string = ""
    for item in response['transcripts'][0]['words']:
        transcript_string = transcript_string+item.get('word')+" "
        if item.get('word') != '': # remove bug
            words_timestamp_list_temp = [item.get('word'), item.get('start_time'), item.get('duration')]
            words_timestamp_list.append(words_timestamp_list_temp)
    transcript_display_list.append(transcript_string)
    return transcript_display_list, confidence_list, words_timestamp_list
