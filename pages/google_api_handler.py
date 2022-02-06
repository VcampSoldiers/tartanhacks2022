import os
import six
import re
from google.cloud import speech_v1, texttospeech, translate_v2


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=""


def speech_to_text(audio):
    config = dict(sample_rate_hertz=44100, language_code="ja-JP", enable_word_time_offsets=True)
    audio = dict(content=audio)
    client = speech_v1.SpeechClient()
    response = client.recognize(config=config, audio=audio)

    return response

def translate_text(target, text):
    translate_client = translate_v2.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    translated_text = re.sub(r"&#39;", "'", result["translatedText"])    

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(translated_text))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

    return translated_text


def text_to_speech(language_code, tmp_dir, idx, text):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        # name='en-US-Wavenet-D',
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
        # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    save_path = os.path.join(tmp_dir, f"google_{idx}.wav")
    with open(save_path, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {save_path}')

    return save_path

langs = ("Albanian",
"Afrikaans",
"Amharic",
"Arabic",
"Armenian",
"Azerbaijani",
"Basque",
"Bengali",
"Bosnian",
"Bulgarian",
"Catalan",
"Chinese ",
"Croatian",
"Czech",
"Danish",
"Dutch",
"English",
"Estonian",
"Finnish",
"French",
"Galician",
"Georgian",
"German",
"Greek",
"Gujarati",
"Hebrew",
"Hindi",
"Hungarian",
"Icelandic",
"Indonesian",
"Italian",
"Japanese",
"Javanese",
"Kannada",
"Kazakh",
"Khmer",
"Korean",
"Lao",
"Latvian",
"Lithuanian",
"Macedonian",
"Malay",
"Malayalam",
"Marathi",
"Mongolian",
"Nepali",
"Norwegian",
"Persian",
"Polish",
"Portuguese ",
"Punjabi",
"Romanian",
"Russian",
"Serbian",
"Sinhala",
"Slovak",
"Slovenian",
"Spanish",
"Sundanese",
"Swahili",
"Swedish",
"Tamil",
"Telugu",
"Thai",
"Turkish",
"Ukrainian",
"Urdu",
"Uzbek",
"Vietnamese",
"Zulu")

def get_language_codes(language):
    if language == "Albanian":
        translate_language_code = "sq"
        voice_language_code = "sq-AL"
    elif language == "Afrikaans":
        translate_language_code = "af"
        voice_language_code = "af-ZA"
    elif language == "Amharic":
        translate_language_code = "am"
        voice_language_code = "am-ET"
    elif language == "Arabic":
        translate_language_code = "ar"
        voice_language_code = "ar-EG"
    elif language == "Armenian":
        translate_language_code = "hy"
        voice_language_code = "hy-AM"
    elif language == "Azerbaijani":
        translate_language_code = "az"
        voice_language_code = "az-AZ"
    elif language == "Basque":
        translate_language_code = "eu"
        voice_language_code = "eu-ES"
    elif language == "Bengali":
        translate_language_code = "bn"
        voice_language_code = "bn-IN"
    elif language == "Bosnian":
        translate_language_code = "bs"
        voice_language_code = "bs-BA"
    elif language == "Bulgarian":
        translate_language_code = "bg"
        voice_language_code = "bg-BG"
    elif language == "Catalan":
        translate_language_code = "ca"
        voice_language_code = "ca-ES"
    elif language == "Chinese ":
        translate_language_code = "zh"
        voice_language_code = "zh"
    elif language == "Croatian":
        translate_language_code = "hr"
        voice_language_code = "hr-HR"
    elif language == "Czech":
        translate_language_code = "cs"
        voice_language_code = "cs-CZ"
    elif language == "Danish":
        translate_language_code = "da"
        voice_language_code = "da-DK"
    elif language == "Dutch":
        translate_language_code = "nl"
        voice_language_code = "nl-NL"
    elif language == "English":
        translate_language_code = "en"
        voice_language_code = "en-US"
    elif language == "Estonian":
        translate_language_code = "et"
        voice_language_code = "et-EE"
    elif language == "Finnish":
        translate_language_code = "fi"
        voice_language_code = "fi-FI"
    elif language == "French":
        translate_language_code = "fr"
        voice_language_code = "fr-FR"
    elif language == "Galician":
        translate_language_code = "gl"
        voice_language_code = "gl-ES"
    elif language == "Georgian":
        translate_language_code = "ka"
        voice_language_code = "ka-GE"
    elif language == "German":
        translate_language_code = "de"
        voice_language_code = "de-DE"
    elif language == "Greek":
        translate_language_code = "el"
        voice_language_code = "el-GR"
    elif language == "Gujarati":
        translate_language_code = "gu"
        voice_language_code = "gu-IN"
    elif language == "Hebrew":
        translate_language_code = "he"
        voice_language_code = "he-IL" 
    elif language == "Hindi":
        translate_language_code = "hi"
        voice_language_code = "hi-IN"
    elif language == "Hungarian":
        translate_language_code = "hu"
        voice_language_code = "hu-HU" 
    elif language == "Icelandic":
        translate_language_code = "ic"
        voice_language_code = "ic-IS"
    elif language == "Indonesian":
        translate_language_code = "in"
        voice_language_code = "in-ID" 
    elif language == "Italian":
        translate_language_code = "it"
        voice_language_code = "it-KE" 
    elif language == "Japanese":
        translate_language_code = "ja"
        voice_language_code = "ja-JP" 
    elif language == "Javanese":
        translate_language_code = "jv"
        voice_language_code = "jv-ID" 
    elif language == "Kannada":
        translate_language_code = "kn"
        voice_language_code = "kn-IN" 
    elif language == "Kazakh":
        translate_language_code = "kk"
        voice_language_code = "kk-KZ" 
    elif language == "Khmer":
        translate_language_code = "km"
        voice_language_code = "km-KH" 
    elif language == "Korean":
        translate_language_code = "ko"
        voice_language_code = "ko-KR"
    elif language == "Lao":
        translate_language_code = "lo"
        voice_language_code = "lo-LA"
    elif language == "Latvian":
        translate_language_code = "lv"
        voice_language_code = "lv-LV"
    elif language == "Lithuanian":
        translate_language_code = "lt"
        voice_language_code = "lt-LT"
    elif language == "Macedonian":
        translate_language_code = "mk"
        voice_language_code = "mk-MK"
    elif language == "Malay":
        translate_language_code = "ms"
        voice_language_code = "ms-MY"
    elif language == "Malayalam":
        translate_language_code = "ml"
        voice_language_code = "ml-IN"
    elif language == "Marathi":
        translate_language_code = "mr"
        voice_language_code = "mr-IN"
    elif language == "Mongolian":
        translate_language_code = "mn"
        voice_language_code = "mn-MN"
    elif language == "Nepali":
        translate_language_code = "ne"
        voice_language_code = "ne-NP"
    elif language == "Norwegian":
        translate_language_code = "no"
        voice_language_code = "no-NO"
    elif language == "Persian":
        translate_language_code = "pe"
        voice_language_code = "pe-IR"
    elif language == "Polish":
        translate_language_code = "pl"
        voice_language_code = "pl-PL"
    elif language == "Portuguese ":
        translate_language_code = "pr"
        voice_language_code = "pr-PT"
    elif language == "Punjabi":
        translate_language_code = "pa"
        voice_language_code = "pa-Guru-IN"
    elif language == "Romanian":
        translate_language_code = "ro"
        voice_language_code = "ro-RO"
    elif language == "Russian":
        translate_language_code = "ru"
        voice_language_code = "ru-RU"
    elif language == "Serbian":
        translate_language_code = "sr"
        voice_language_code = "sr-RS"
    elif language == "Sinhala":
        translate_language_code = "si"
        voice_language_code = "si-LK"
    elif language == "Slovak":
        translate_language_code = "sk"
        voice_language_code = "sk-SK"
    elif language == "Slovenian":
        translate_language_code = "sl"
        voice_language_code = "sl-SI"
    elif language == "Spanish":
        translate_language_code = "es"
        voice_language_code = "es-ES"
    elif language == "Sundanese":
        translate_language_code = "su"
        voice_language_code = "su-ID"
    elif language == "Swahili":
        translate_language_code = "sw"
        voice_language_code = "sw-KE"
    elif language == "Swedish":
        translate_language_code = "sv"
        voice_language_code = "sv-SE"
    elif language == "Tamil":
        translate_language_code = "ta"
        voice_language_code = "ta-IN"
    elif language == "Telugu":
        translate_language_code = "te"
        voice_language_code = "te-IN"
    elif language == "Thai":
        translate_language_code = "th"
        voice_language_code = "th-TH"
    elif language == "Turkish":
        translate_language_code = "tr"
        voice_language_code = "tr-TR"
    elif language == "Ukrainian":
        translate_language_code = "uk"
        voice_language_code = "uk-UA"
    elif language == "Urdu":
        translate_language_code = "ur"
        voice_language_code = "ur-PK"
    elif language == "Uzbek":
        translate_language_code = "uz"
        voice_language_code = "uz-UZ"
    elif language == "Vietnamese":
        translate_language_code = "vi"
        voice_language_code = "vi-VN"
    elif language == "Zulu":
        translate_language_code = "zu"
        voice_language_code = "zu-ZA"

    return translate_language_code, voice_language_code