from google.cloud import storage, speech_v1
from utils import *

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print(f"deleted.....'{blob_name}'")


def upload_files_to_bucket(TESTCASES, BUCKET_NAME, BUCKET_PATH):
    for t in TESTCASES:    
        #set save path
        destination_blob_name = BUCKET_PATH + t['filename']
        #try upload
        print (f"uploading..... {t['filename']}")
        try:
            upload_blob(bucket_name = BUCKET_NAME,
                        source_file_name = t['full_path'],
                        destination_blob_name = destination_blob_name)
        except:
            print(f"Upload failed: {t['filename']}")


def google_batch_stt(t, BUCKET_NAME, BUCKET_PATH) -> str:
    full_path = t['full_path'],
    path, filename = os.path.split(full_path[0])
    lang = t['lang'][0],
    encoding = t['encoding']
    
    buffer, rate = read_wav_file(full_path[0])
    client = speech_v1.SpeechClient()

    config = {
        'language_code': lang,
        'encoding': speech_v1.RecognitionConfig.AudioEncoding[encoding],
        "enable_word_time_offsets": True
    }

    audio = {
        'content': buffer
    }

    # Set the path
    gcs_uri = "gs://"+ BUCKET_NAME +"/"+ BUCKET_PATH + filename
    # Get the audio item
    audio = speech_v1.RecognitionAudio(uri=gcs_uri)
    
    # For short audio file.
    # response = client.recognize(config=config, audio=audio)
    # For bigger audio file, the previous line can be replaced with following:
    try:
        operation = client.long_running_recognize(config=config, audio=audio)
    except:
        # if it is sample_rate_hertz issue, try again with 16000 hertz
        print("...Second try from exception clause...")
        config = {
            'language_code': lang,
            'encoding': speech_v1.RecognitionConfig.AudioEncoding[encoding],
            'sample_rate_hertz': 16000,
            "enable_word_time_offsets": True
        }
        try:
            operation = client.long_running_recognize(config=config, audio=audio)
        except:
            print("...Even Secend has failed... skip this file..")
            return ["Failed file"],[1],[]
    
    response = operation.result()

    # save result in text
    save_to_text(path, filename, "google", str(response))

    # space for results
    transcripts = []
    confidences = []
    word_timestamp = []

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        # Save transcripts in list
        transcripts.append(alternative.transcript)
        print(alternative.transcript)
        confidences.append(alternative.confidence)

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            duration = end_time-start_time
            
            #Save in list
            word_timestamp.append([word,
                                start_time.total_seconds(),
                                duration.total_seconds(),])

    return transcripts, confidences, word_timestamp