import sys
print(sys.path)

"""
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname
import json
with open("ibm-credentials.json") as file:
    ibm_credentials = json.load(file)
    APIKEY = ibm_credentials.get("apiKey")
    URL = ibm_credentials.get("url")

speech_to_text = SpeechToTextV1(
    iam_apikey=APIKEY,
    url=KEY
)

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

myRecognizeCallback = MyRecognizeCallback()

with open(join(dirname(__file__), './.', 'male.wav'),
              'rb') as audio_file:
    audio_source = AudioSource(audio_file)
    speech_to_text.recognize_using_websocket(
        audio=audio_source,
        content_type='audio/wav',
        recognize_callback=myRecognizeCallback,
        model='en-US_BroadbandModel')
"""