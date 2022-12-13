FILE_PATH = "/path/to/database/source_dir"

import time
from utils import *
from azure_utils import *

# Get audio files from path
files = check_file_path(FILE_PATH)
TESTCASES = define_test_cases(files)

# API KEY SETTING
AZURE_KEY = ''
AZURE_SERVICE_REGION = 'australiaeast'

# Ready CSV to save result
csv_f = create_csv_file(FILE_PATH, "ms_api")
cnt = 1

# Run
for t in TESTCASES:
    print('[{1}/{2}]MS Processing audio file "{0}"'.format(t['filename'],cnt,len(TESTCASES)))
    
    transcripts,confidences,word_timestamp = from_file(t['full_path'], AZURE_KEY, AZURE_SERVICE_REGION)
    export_result_csv(csv_f, t['filename'],transcripts,confidences,word_timestamp)

    cnt += 1


