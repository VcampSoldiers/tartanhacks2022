import os
from google.cloud import speech_v1, texttospeech 
from googletrans import Translator

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="tartanhacks2022-340415-76005c636c36.json"


def speech_to_text(audio):
    config = dict(sample_rate_hertz=44100, language_code="ja-JP", enable_word_time_offsets=True)
    audio = dict(content=audio)
    client = speech_v1.SpeechClient()
    response = client.recognize(config=config, audio=audio)

    return response

def translate_text(target, text):
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    

    return result["translatedText"]


# def translate_text(text):
#     translator = Translator()
#     result = translator.translate(text, dest="en")
#     return result[0]

def text_to_speech(idx, text):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-C',
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        # ssml_gender=texttospeech.SsmlVoiceGender.MALE)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(f'google_{idx}.wav', 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file google_{idx}.mp3')

    return f"google_{idx}.wav"