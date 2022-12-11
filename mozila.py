# FILE_PATH = "/home/mirap/0_DATABASE/TalkBank_dataset/train_assorted/Full_wave_enhanced_audio/cd/"
FILE_PATH = "/home/mirap/0_DATABASE/island_wav/1_picture_describing_test/"
DEEPSPEECH_MODEL_PATH = "/home/mirap/0_DATABASE/Mozila/deepspeech-0.9.3-models.pbmm"

from utils import *
from mozila_utils import *
import deepspeech

# Get audio files from path
files = check_file_path(FILE_PATH)
TESTCASES = define_test_cases(files)

# Set Deepspeech model
model = deepspeech.Model(DEEPSPEECH_MODEL_PATH)

# Ready CSV file to save result
csv_f = create_csv_file(FILE_PATH, "deepspeech_api")
cnt = 1

# Run
for t in TESTCASES:
    print('[{1}/{2}]DS Processing audio file "{0}"'.format(t['filename'],cnt,len(TESTCASES)))
    
    output = deepspeech_batch_stt(model, t['full_path'])
    json_output = metadata_json_output(output)
    
    # save the result
    save_to_json(FILE_PATH, t['filename'], "ds", json_output)
    transcripts,confidences,word_timestamp = extract_from_json_deepspeech(json_output)
    export_result_csv(csv_f, t['filename'], transcripts, confidences, word_timestamp)

    cnt += 1

