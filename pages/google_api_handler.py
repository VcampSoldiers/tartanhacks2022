import os
from google.cloud import speech_v1, texttospeech 
from googletrans import Translator

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="local-alignment-229405-77ff2112f7b2.json"


def speech_to_text(audio):
    config = dict(sample_rate_hertz=44100, language_code="ja-JP")
    audio = dict(content=audio)
    client = speech_v1.SpeechClient()
    response = client.recognize(config=config, audio=audio)
    return response

def translate_text(text):
    translator = Translator()
    result = translator.translate(text, dest="en")
    return result[0]

def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-C',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')