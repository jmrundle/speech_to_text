from ibm_watson import SpeechToTextV1
from os.path import join, dirname
import json

# base url for Dallas hosting location
base_url = "stream.watsonplatform.net"
# format base url into speech-to-text endpoint 
URL = "wss://{base_url}/speech-to-text/api/v1/recognize".format(base_url=base_url)

# load api key from json file
with open("ibm-credentials.json") as file:
    ibm_credentials = json.load(file)
    APIKEY = ibm_credentials.get("apiKey")

# speech to text object
speech_to_text = SpeechToTextV1(
    iam_apikey=APIKEY,
    url=KEY
)

class AudioSource(object):
    def __init__(self, input, is_recording=False, is_buffer=False):
        self.input = input
        self.is_recording = is_recording
        self.is_buffer = is_buffer
    def completed_recording(self):
        self.is_recording = False

# customized callback functions
class RecognizeCallback(object):
    def __init__(self):
        pass

    def on_data(self, data):
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))
    
    def on_transcription(self, transcript):
        pass

    def on_connected(self):
        pass

    def on_listening(self):
        pass

    def on_hypothesis(self, hypothesis):
        pass

    def on_close(self):
        pass

RecognizeCallback = RecognizeCallback()

with open(join(dirname(__file__), './.', 'en-US_Broadband_sample1.wav'),
              'rb') as audio_file:
    audio_source = AudioSource(audio_file)
    speech_to_text.recognize_using_websocket(
        audio=audio_source,
        content_type='audio/wav',
        recognize_callback=RecognizeCallback,
        model='en-US_BroadbandModel')
