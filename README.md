# Speech to text with meta data 🗣👂📝
This implementation convert speech audio data (.wav) into text transcript with meta data. The meta data include many useful speech features such as **length of pause, speed of speech and the number of most spoken word**. These data will be useful to train AI for linear regression or classfication. The transcript can be extracted by 3 different API: **Google**, **Azure**, and **Mozila(Deep Speech)**. Hope one of these works on your project!

## Usage
🌐 Google speech to text
- first, get API key (json) from : https://cloud.google.com/speech-to-text/
- configure path and API path in google_run.py
```
python google_run.py
```
\
Ⓜ️ Mozila Deep speech
- first, get pre-trained model from : [Mozila Releases](https://github.com/mozilla/DeepSpeech/releases)
- for further tutorial check : [Mozila tutorial page](https://deepspeech.readthedocs.io/en/latest/USING.html)
- install deep speech
```
pip install deepspeech
```
- configure path in mozila.py
```
python mozila.py
```
\
🅰️ Azure speech to text
- first, get API key form : [MS Azure page](https://azure.microsoft.com/en-us/products/cognitive-services/speech-to-text)
- configure path and API path in azure_ms.py
```
python azure_ms.py
```

## extractable features
- durations : 
- start_times : start time of speech
- confidence_mean
- confidence_median
- number_of_words
- types_of_words
- duplicated_words
- types_of_words_mode (number of most spoken word)
- length_of_audio (total length of the audio file)
- length_of_speech
- number_of_words_per_second_in_total = number_of_words/length_of_audio
- number_of_words_per_second_in_speech = number_of_words/length_of_speech
- speed_of_speech_mean
- length_of_pause = round(length_of_audio - length_of_speech,4)
- propotion_of_pause = round(length_of_pause / length_of_audio,4)
    
## features to be impelemented..
- length_of_pause_mean = length_of_pause / number_of_sentence?
- max_words_in_a_sentence
- avg_words_in_a_sentence
- medium_words_in_a_sentence
- max_durataion_of_a_sentence
- avg_durateion_of_a_sentence
- duration_of_a_sentence_medium
- speed_of_a_sentence->max,medium...

## memo
The transcripts and features will be saved into csv format.
