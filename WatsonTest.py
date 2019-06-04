from watson_developer_cloud import SpeechToTextV1
from ws4py.client.threadedclient import WebSocketClient
import json


class User(object):
    def __init__(self, 
                 username=None,
                 password=None,
                 api_key=None,
                 json_file="ibm-credentials.json"):
        """
        Three ways to connect with Watson API:
            1. pass your IBM API key into User class initialization
            2. pass your IBM username and password into User class initialization
            3. fill login credentials into ibm-credentials.json file within directory
        """
        self.username = username
        self.password = password
        self.api_key = api_key

        if api_key is None and (username is None or password is None):
            self.import_credentials_from_json(json_file)
        else:
            raise ValueError('Login requires a username-password combo or an API key')

    def import_credentials_from_json(self, json_file):
        """checks ibm-credentials.json file for Watson-API login credentials"""
        try:
            with open(json_file) as file:
                try:
                    ibm_credentials = json.load(file)
                except AttributeError:
                    raise ValueError('File is not in JSON format')
                self.api_key = ibm_credentials.get("apiKey")
                self.username = ibm_credentials.get("username")
                self.password = ibm_credentials.get("password")
        except FileNotFoundError:
            raise ValueError('JSON file not found.  Fill your login credentials into the ibm-credentials.json file.')

    def recognize_upload(self, audio, **kwargs):
        """gets Watson-API JSON response from an audio file upload"""
        
        # filter param input
        params = kwargs
        if 'content_type' not in kwargs:
            params['content_type'] = 'audio/wav'
        if 'model' not in kwargs:
            params['model'] = 'en-US_NarrowbandModel' if params['content_type'] == 'audio/mp4' else 'en-US_BroadbandModel'

        self.url = "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
        self.stt = self.get_watson_stt_object()

        # open audio file and run analysis using Watson speech-to-text method
        with open(audio, 'rb') as audio_file:
            return self.stt.recognize(audio_file, **params).get_result()

    def get_watson_stt_object(self):
        """create Watson speech-to-text object"""
        stt = None
        if self.api_key is not None:
            stt = SpeechToTextV1(
                iam_apikey=self.api_key)
        elif self.username is not None and self.password is not None:
            stt = SpeechToTextV1(
                username=self.username,
                password=self.password)
        return stt

    def get_transcript(self, audio, **kwargs):
        """Transcribes audio from a file upload"""
        response = self.recognize_upload(audio, **kwargs)
        try:
            transcript = response["results"][0]["alternatives"][0]["transcript"]
            print(transcript)
            return transcript
        except KeyError:
            print("Error transcribing audio")


if __name__ == '__main__':
    user = User()
    user.get_transcript('male.wav', model='en-US_NarrowbandModel')
