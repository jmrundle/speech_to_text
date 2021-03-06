#!/usr/bin/env python3

from watson_developer_cloud import SpeechToTextV1
import json
import os
import sys


class WatsonWrapper(object):
    url = "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"

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

        # check json_file if no api_key or username-password is provided
        if api_key is None and (username is None or password is None):
            self.import_credentials_from_json(json_file)

        # raise error if json_file did not have necessary information
        if api_key is None and (username is None or password is None):
            print("Login requires a username-password combo or an API key")
            sys.exit(1)

        self.stt = self.get_watson_stt_object()

    def import_credentials_from_json(self, json_file):
        """checks ibm-credentials.json file for Watson-API login credentials"""
        try:
            with open(json_file) as file:
                try:
                    ibm_credentials = json.load(file)
                except AttributeError:
                    print("File is not in JSON format")
                    sys.exit(1)

                self.api_key = ibm_credentials.get("apiKey")
                self.username = ibm_credentials.get("username")
                self.password = ibm_credentials.get("password")

        except FileNotFoundError:
            print("JSON file not found.  Fill your login credentials into the ibm-credentials.json file.")
            sys.exit(1)

    def recognize_upload(self, audio, params={}):
        """gets Watson-API JSON response from an audio file upload"""
        
        # filter and set param input
        if 'content_type' not in params:
            params['content_type'] = 'audio/wav'
        if 'model' not in params:
            params['model'] = 'en-US_NarrowbandModel' if params['content_type'] == 'audio/mp4' else 'en-US_BroadbandModel'

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
        response = self.recognize_upload(audio, params=kwargs)
        try:
            return response["results"][0]["alternatives"][0]["transcript"]
        except KeyError:
            print("Error transcribing audio")
            sys.exit(2)

    def get_speaker_transcript(self, audio, **kwargs):
        """Seperates audio into an array of speakers and transcript"""
        kwargs['speaker_labels'] = True
        response = self.recognize_upload(audio, params=kwargs)

        # timestamps for each word
        timestamps = response["results"][0]["alternatives"][0]["timestamps"]
        # speaker labels for each timestamp
        speaker_labels = response["speaker_labels"]

        print("Speaker 1:", end="")  # first speaker tag
        
        transcript = []
        speaker = 0                 # assign first speaker number
        phrase = ""                 # assign first speaker phrase
        
        for wordInfo, speakerInfo in zip(timestamps, speaker_labels):
            # same speaker
            if int(speakerInfo['speaker']) == speaker:
                phrase += " " + wordInfo[0]

            # new speaker
            else:
                print(phrase)
                transcript.append([speaker, phrase.strip()])
                
                speaker = int(speakerInfo['speaker'])
                print("Speaker {}: ".format(speaker + 1), end="")
                phrase = wordInfo[0]
        
        print(phrase)
        transcript.append([speaker, phrase.strip()])
        
        return transcript


def _get_file_names(file_type, directory="."):
    """Returns iterator (map object) of all file names with a specified extension within specified directory"""
    # read in all files within dir
    try:
        entries = os.listdir(directory)
    except OSError:
        print(f"Specified audio directory ({directory}) does not exist")
        sys.exit(3)

    # all files of specified type
    files = filter(lambda f: os.path.splitext(f)[1] == file_type, entries)

    # prepend directory name
    return map(lambda f: os.path.join(directory, f), files)


def get_audio_files(file_type=".wav", directory="audio"):
    return _get_file_names(file_type, directory)


if __name__ == '__main__':
    wrapper = WatsonWrapper()

    for file_name in get_audio_files():
        print('Processing ' + file_name + '...\n')

        wrapper.get_speaker_transcript(file_name)

        print('\n')
