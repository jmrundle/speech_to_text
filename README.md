# Speech to Text using IBM-Watson API
Implements various functions as a means to test features of the IBM-Watson speech to text utility 

### Usage as a Package

```python
import SpeechToText
wrapper = SpeechToText.WatsonWrapper(api_key="yourApiKey")

for sample in SpeechToText.get_audio_files():
    wrapper.get_speaker_transcript(sample)
```
