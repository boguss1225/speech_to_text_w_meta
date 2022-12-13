from utils import *
from google_utils import *

FILE_PATH = "/path/to/database/source_dir"

API_KEY = '/path/to/api/dir/googleapikey.json'

BUCKET_NAME = "google_bucket_name"
BUCKET_PATH = "bucket_name/"

# Get audio files from path
files = check_file_path(FILE_PATH)
TESTCASES = define_test_cases(files)

# Set API_KEY
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = API_KEY

# Upload files to Bucket
upload_files_to_bucket(TESTCASES, BUCKET_NAME, BUCKET_PATH)

# Ready CSV to save result
csv_f = create_csv_file(FILE_PATH, "google_api")
cnt = 1

# Run
for t in TESTCASES:
    print('[{1}/{2}] [Google] Processing audio file "{0}"'.format(t['filename'],cnt,len(TESTCASES)))

    transcripts, confidences, word_timestamp = google_batch_stt(
    	t, BUCKET_NAME, BUCKET_PATH)

    export_result_csv(csv_f,t['filename'],transcripts,confidences,word_timestamp)

    # delete used file from bucket
    destination_blob_name = BUCKET_PATH + t['filename']
    delete_blob(BUCKET_NAME, destination_blob_name)

    cnt += 1
