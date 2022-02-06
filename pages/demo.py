import os
import shutil
import subprocess

import streamlit as st
import moviepy.editor as mp
from moviepy.audio.io.AudioFileClip import AudioFileClip

from pages.google_api_handler import speech_to_text, translate_text, text_to_speech, langs, get_language_codes


tmpDir = "temp"
temp_input_video_path = os.path.join(tmpDir, "temp_input.mp4")
temp_source_audio_path = os.path.join(tmpDir, "temp_source.mp3")
temp_target_audio_path = os.path.join(tmpDir, "temp_target.mp3")
temp_processed_audio_path = os.path.join(tmpDir, "temp_output.wav")
temp_output_video_path = os.path.join(tmpDir, "temp_output.mp4")

chunk_duration = 5

def make_silence_audio(duration):
    duration = (duration > 0) * duration  
    return mp.AudioClip(make_frame = lambda t: 0, duration=duration, fps=44100)

def process_audio(src_audio, tgt_audio):
    # Add silent padding
    temp_src_audio = AudioFileClip(src_audio)
    silence_duration = (temp_src_audio.duration < 5) * (5-temp_src_audio.duration)
    silence = mp.AudioClip(make_frame = lambda t: 0, duration=0.5+silence_duration, fps = 44100)
    temp_src_audio = mp.concatenate_audioclips([silence,temp_src_audio])
    temp_src_audio.write_audiofile(src_audio)
    
    tgt_audio.write_audiofile(temp_target_audio_path)
    popen = subprocess.Popen(f"python3 audio_handler/FragmentVC/convert.py -w audio_handler/wav2vec_small.pt -v audio_handler/vocoder.pt -c audio_handler/fragmentvc.pt {src_audio} {temp_target_audio_path} {temp_target_audio_path} {temp_target_audio_path} -o {temp_processed_audio_path}", shell=True)
    popen.wait()
    return AudioFileClip(temp_processed_audio_path)

def resize_audio(audio, target_length):
    temp_clip = mp.ColorClip(size=(1,1), color=(0,0,0), duration=audio.duration)
    temp_clip = temp_clip.set_audio(audio)
    temp_clip = temp_clip.fx(mp.vfx.speedx, audio.duration/target_length)
    audio = temp_clip.audio
    return audio

def split_text(text):
    # Get list of words
    words = text.results[0].alternatives[0].words
    start_time = words[0].start_time.seconds
    splitted_text = []
    start_times = [start_time]
    temp_str = ""
    for w in words:
        if w.start_time.seconds >= start_time+5:
            splitted_text.append(temp_str)
            temp_str = ""
            start_time = w.start_time.seconds
            start_times.append(start_time)
        temp_str += (w.word.split("|")[0])

    splitted_text.append(temp_str)
    print(f"Splitted Text: {splitted_text}")
    return splitted_text, start_times


def app():
    option = st.selectbox(
        'Choose target language',
        langs)
    st.write('You selected:', option)

    # Upload video
    file = st.file_uploader("Upload video", type="mp4")

    if file:
        os.makedirs(tmpDir, exist_ok=True)

        # Read video
        video_bytes = file.read()

        # Save as temp file
        with open(temp_input_video_path, 'wb') as wfile:
            wfile.write(video_bytes)

        # Extract audio 
        temp_clip = mp.VideoFileClip(temp_input_video_path)

        translate_language_code, voice_language_code = get_language_codes(option)
        translated_audio = os.path.join("language_files", f"{translate_language_code}.wav")

        temp_clip.audio.write_audiofile(temp_source_audio_path)
        # Extract text and timestamps
        with open(temp_source_audio_path, 'rb') as fd:
            enc = fd.read()

        text = speech_to_text(enc)
        transcript = ""
        for r in text.results:
            transcript += r.alternatives[0].transcript
        start_time = (text.results[0].alternatives[0].words[0].end_time).total_seconds() - 1
        end_time = text.results[-1].result_end_time.total_seconds()
        
        translated_text = translate_text(translate_language_code, transcript)

        if os.path.isfile(translated_audio):
            new_audio = AudioFileClip(translated_audio)
        else:
            eng_voice_path = text_to_speech(voice_language_code, tmpDir, 0, translated_text)
            new_audio = process_audio(eng_voice_path,temp_clip.audio.subclip(start_time, end_time))
            new_audio = resize_audio(new_audio, end_time-start_time)

            start_silence = temp_clip.audio.subclip(0, start_time)
            new_audio = mp.concatenate_audioclips([start_silence, new_audio])

            new_audio.write_audiofile(translated_audio)

        # Overlap video with new audio
        final_clip = temp_clip.set_audio(new_audio)
        final_clip.write_videofile(temp_output_video_path, fps=30,codec="libx264",audio_codec='aac')

        # Show both videos
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("Original Video")
                st.video(video_bytes)

                st.subheader('Original Text:')
                st.write(transcript)

            with col2:
                st.header("Processed Video")
                st.video(temp_output_video_path)

                st.subheader('Translated Text')
                st.write(translated_text)
        
        shutil.rmtree(tmpDir)