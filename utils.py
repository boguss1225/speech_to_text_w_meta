import os
from typing import Tuple
from csv import writer
import numpy as np
import wave
import sys
import datetime
import json
from scipy import stats

def check_file_path(FILE_PATH):
	if(os.path.isfile(FILE_PATH)):
	    print("Please give directory path! Not file path!")
	    sys.exit()

	if(os.path.isdir(FILE_PATH)):
	    import glob
	    files=glob.glob(FILE_PATH + "/*.wav")
	    return files

def define_test_cases(files):
	TESTCASES = []

	for file in files:
	    # split path and filename
	    path, audio_filename = os.path.split(file)

	    TESTCASES.append({
	    'full_path': file,
	    'filename': audio_filename,
	    'encoding': 'LINEAR16',
	    'lang': 'en-AU'
  	})

	return TESTCASES

def read_wav_file(filename) -> Tuple[bytes, int]:
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)

    return buffer, rate

def simulate_stream(buffer: bytes, batch_size: int = 4096):
    buffer_len = len(buffer)
    offset = 0
    while offset < buffer_len:
        end_offset = offset + batch_size
        buf = buffer[offset:end_offset]
        yield buf
        offset = end_offset

def create_csv_file(FILE_PATH, filename_head) :
    # randomise csv filename according to time of creation
    time = datetime.datetime.now()
    filename = FILE_PATH +"/"+ filename_head + time.strftime("%d%H%M") +".csv"
    # check duplication
    if( os.path.isfile(filename) ):
        print(f"the file - {filename} already exist")
        sys.exit()
    
    f = open(filename,"w")
    f.close()
    
    return filename

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow([list_of_elem])

def export_result_csv(csv_filename,audio_filename,transcripts,confidences,word_timestamp):
    full_transcripts = ' '.join(transcripts)
    # split word_timestamp array
    word_data = np.array(word_timestamp)
    try:
        words, start_times, durations = word_data.T
    except:
        words, start_times, durations = np.array(["errorfile"]),np.array([0]),np.array([0])
    durations = durations.astype('float64')
    start_times = start_times.astype('float64')
    # calculate values
    confidence_mean = round(np.mean(confidences),4)
    confidence_median = round(np.median(confidences),4)
    number_of_words = len(word_timestamp)
    types_of_words = len(np.unique(words))
    # duplicated_words = number_of_words-types_of_words
    types_of_words_mode = stats.mode(words).count[0]
    length_of_audio = round(start_times[-1] + durations[-1],4)
    length_of_speech = round(np.sum(durations),4)
    number_of_words_per_second_in_total = number_of_words/length_of_audio
    number_of_words_per_second_in_speech = number_of_words/length_of_speech
    # length_of_sentence_mean = np.mean(start_times) #
    speed_of_speech_mean = round(length_of_speech / number_of_words,4)
    # speed_of_speech_max = max_length_of_sentence / number_of_words_from_max_sentence
    length_of_pause = round(length_of_audio - length_of_speech,4)
    propotion_of_pause = round(length_of_pause / length_of_audio,4)
    # length_of_pause_mean = length_of_pause / number_of_sentence?
    # max_words_in_a_sentence
    # avg_words_in_a_sentence
    # medium_words_in_a_sentence
    # max_durataion_of_a_sentence
    # avg_durateion_of_a_sentence
    # duration_of_a_sentence_medium
    # speed_of_a_sentence->max,mean,medium...

    print("  confidence_mean:",confidence_mean,
        "\n  confidence_median:",confidence_median,
        "\n  number_of_words:",number_of_words,
        "\n  types_of_words:",types_of_words,
        # "\n  duplicated_words:",duplicated_words,
        "\n  types_of_words_mode:",types_of_words_mode,
        "\n  length_of_audio:",length_of_audio,
        "\n  length_of_speech:",length_of_speech,
        "\n  speed_of_speech_mean:",speed_of_speech_mean,
        "\n  length_of_pause:",length_of_pause,
        "\n  propotion_of_pause:",propotion_of_pause)

    contents = str(audio_filename) + ";"
    contents += str(full_transcripts) + ";"
    contents += str(confidence_mean) + ";"
    contents += str(confidence_median) + ";"
    contents += str(number_of_words) + ";" # word count from transcripts
    contents += str(types_of_words) + ";" # word type count from transcripts
    # contents += str(duplicated_words) + ";" 
    contents += str(types_of_words_mode) + ";" # mode of words type
    contents += str(length_of_audio) + ";" # total time of audio duration
    contents += str(length_of_speech) + ";" # sum of speech duration
    contents += str(number_of_words_per_second_in_total) + ";"
    contents += str(number_of_words_per_second_in_speech) + ";"
    # contents += number_of_sentence + ";" # 
    # contents += length_of_sentence_mean + ";" # mean number of words from sentences
    # contents += length_of_sentence_median + ";" # median number of words from sentences
    # contents += length_of_sentence_max + ";" # max number of words from sentences
    contents += str(speed_of_speech_mean) + ";" # length_of_speech / number_of_words
    # contents += speed_of_speech_max + ";" # max_length_of_sentence / number_of_words_from_max_sentence
    contents += str(length_of_pause) + ";" # length_of_audio - length_of_speech
    # contents += length_of_pause_mean + ";" # (length_of_audio - length_of_speech) / number_of_sentence
    contents += str(propotion_of_pause) + ";" # length_of_pause / length_of_audio

    # Open file in append mode
    with open(csv_filename, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow([contents])

def save_to_text(FILE_PATH, filename, format, data):
    dst_path = FILE_PATH +"/"+format
    filename = dst_path+"/"+format+"_"+filename+".txt"
    
    if not os.path.exists(dst_path):
        print("making dir for..",dst_path)
        os.makedirs(dst_path)

    f = open(filename, 'w')
    f.write(data)
    print("saved in text file:",filename)

def save_to_json(FILE_PATH, filename, format, data):
    dst_path = FILE_PATH +"/"+format
    filename = dst_path+"/"+format+"_"+filename+".json"

    if not os.path.exists(dst_path):
        print("making dir for..",dst_path)
        os.makedirs(dst_path)

    f = open(filename, 'w')
    data = json.loads(data)
    json.dump(data, f)
    print("saved in json file:",filename)