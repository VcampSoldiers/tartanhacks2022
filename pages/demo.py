import os
import subprocess
import cv2
import time
import numpy as np
import streamlit as st
import moviepy.editor as mp
import base64 
from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pages.google_api_handler import speech_to_text, translate_text, text_to_speech


temp_input_video_path = "temp.mp4"
# temp_audio_path = "google.wav"
temp_output_video_path = "temp_output.mp4"
chunk_duration = 5

def process_audio(src_audio, tgt_audio):
    temp_target_path = "asdf.wav"
    tgt_audio.write_audiofile(temp_target_path)

    # popen = subprocess.Popen(f"python3 audio_handler/FragmentVC/convert.py -w audio_handler/wav2vec_small.pt -v audio_handler/vocoder.pt -c audio_handler/fragmentvc.pt --sample_rate 44100 {src_audio} {temp_target_path} -o output.wav", shell=True)
    # # popen = subprocess.Popen(f"python3 audio_handler/FragmentVC/convert.py -w audio_handler/wav2vec_small.pt -v audio_handler/vocoder.pt -c audio_handler/fragmentvc.pt {src_audio} {temp_target_path}", shell=True)
    # popen.wait()

    os.system(f"python3 audio_handler/FragmentVC/convert.py -w audio_handler/wav2vec_small.pt -v audio_handler/vocoder.pt -c audio_handler/fragmentvc.pt {src_audio} {temp_target_path}")
    time.sleep(120)

    return AudioFileClip("output.wav")


def split_text(text):
    return [text]
    # words = text.split()
    # output = []

    # word_length = len(words)
    # for i in range(len(words)/2 - 1):
    #     output.append(words[i]+' '+words[i+1])


def app():
    # Upload video
    file = st.file_uploader("Upload video", type="mp4")

    if file:
        # Read video
        video_bytes = file.read()

        # Save as temp file
        with open(temp_input_video_path, 'wb') as wfile:
            wfile.write(video_bytes)

        # Extract audio 
        temp_clip = mp.VideoFileClip(temp_input_video_path)
        temp_clip.audio.write_audiofile("google_cloud.mp3")    

        # Extract text and timestamps
        with open("google_cloud.mp3", 'rb') as fd:
            enc = fd.read()

        text = speech_to_text(enc)
        
        transcript = text.results[0].alternatives[0].transcript
        splitted_texts = split_text(transcript)
        splitted_texts = [translate_text("en", splitted_text) for splitted_text in splitted_texts]
        eng_voice_paths = [text_to_speech(idx,splitted_text) for idx,splitted_text in enumerate(splitted_texts)]
        new_audio = [process_audio(AudioFileClip(eng_voice_path),temp_clip.audio) for eng_voice_path in eng_voice_paths]

        # new_audio = process_audio(AudioFileClip(eng_voice_paths[0]),temp_clip.audio)
        # video_split_interval = temp_clip.duration // len(splitted_texts)

        # start_sec = 0
        # end_sec = video_split_interval
        
        # new_audio = []
        # while (start_sec < temp_clip.duration):
        #     # Split and process audio
        #     new_audio.append(process_audio(temp_clip.audio.subclip(start_sec, end_sec)))

        #     start_sec += video_split_interval
        #     end_sec += video_split_interval

        #     if (end_sec > temp_clip.duration):
        #         end_sec = temp_clip.duration

        new_audio = mp.concatenate_audioclips(new_audio)


        # for audio_chunk in temp_clip.audio.iter_chunks(chunk_duration = 1, nbytes=2,fps=44100):
        #     print(audio_chunk.shape)
        #     # new_chunk = AudioArrayClip(audio_chunk, fps=44100)
        #     # new_chunk = process_audio(new_chunk)
        #     # new_audio.append(new_chunk)
        # new_audio = mp.concatenate_audioclips(new_audio)

        # Overlap video with new audio
        final_clip = temp_clip.set_audio(new_audio)
        final_clip.write_videofile(temp_output_video_path, fps=30,codec="libx264",audio_codec='aac')

        # Show both videos
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("Original Video")
                st.video(video_bytes)

            with col2:
                st.header("Processed Video")
                st.video(temp_output_video_path)