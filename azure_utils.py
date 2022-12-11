import json
import os
import time
import azure.cognitiveservices.speech as speechsdk

from utils import *

def extract_from_json(JSON_DATA, transcript_display_list, words_timestamp_list ,confidence_list):
    DEV=10000000
    response = json.loads(JSON_DATA)
    transcript_display_list.append(response['DisplayText'])
    confidence_list_temp = [item.get('Confidence') for item in response['NBest']]
    max_confidence_index = confidence_list_temp.index(max(confidence_list_temp))
    confidence_list.append(response['NBest'][max_confidence_index]['Confidence'])
    for item in response['NBest'][max_confidence_index]['Words']:
        words_timestamp_list_temp = [item.get('Word'), item.get('Offset')/DEV, item.get('Duration')/DEV]
        words_timestamp_list.append(words_timestamp_list_temp)

def from_file(FILE_PATH, AZURE_SPEECH_KEY, AZURE_SERVICE_REGION):
    path, filename = os.path.split(FILE_PATH)
    json_output = []
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SERVICE_REGION)
    
    speech_config.request_word_level_timestamps()
    speech_config.output_format = speechsdk.OutputFormat(1)

    audio_config = speechsdk.AudioConfig(filename=FILE_PATH)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # save the result
    transcript_display_list = []
    confidence_list = []
    words_timestamp_list = []

    speech_recognizer.recognized.connect(lambda evt: extract_from_json(
        evt.result.json,
        transcript_display_list,
        words_timestamp_list,
        confidence_list
    ))
    # save result in json
    speech_recognizer.recognized.connect(lambda evt: json_output.append(evt.result.json))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    speech_recognizer.stop_continuous_recognition()

    save_to_text(path, filename,"ms",str(json_output))

    return transcript_display_list,confidence_list,words_timestamp_list