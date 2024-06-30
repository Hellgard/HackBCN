  ###################################### SimplifAI ##########################################
##                                File for HackBCN EVENT                                   ##
##                                     Author: Erwan                                       ##
##                                   Date: 2024-06-29                                      ##
##                                     Version: 1.0                                        ##
##                                Python Version: 3.10.11                                  ##
  ###################################### SimplifAI ##########################################

import numpy as np
import soundfile as sf
from openai import OpenAI
client = OpenAI( api_key="sk-proj-289D4ZJKvKBKWy3zgSRcT3BlbkFJgg2WVUltqQxyMB0i2JE1")
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import os
import pygame
import openai
import speech_recognition as sr
from gtts import gTTS
import requests

def split_text(text, max_length):
    """Splits the text into chunks of max_length characters."""
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def TextToSpeech2(robot):
    text = str(robot.robot_response.response.choices[0].message.content)
    chunks = split_text(text, 500)  # Split text into 500 character chunks

    for chunk in chunks:
        response = requests.post(
            'https://api.v6.unrealspeech.com/stream',
            headers={
                'Authorization': 'Bearer ovajYmFzkNXEj2qocfi5nH5MORQRlEhpqY4dEfdwTZp1TvBzPf4UiY'
            },
            json={
                'Text': chunk,
                'VoiceId': 'Amy',  # Dan, Will, Scarlett, Liv, Amy
                'Bitrate': '64k',  # 320k, 256k, 192k, ...
                'Speed': '0',  # -1.0 to 1.0
                'Pitch': '1',  # -0.5 to 1.5
                'Codec': 'libmp3lame',  # libmp3lame or pcm_mulaw
            }
        )

        if response.status_code != 200:
            print("Error: Failed to get a valid response from the API")
            print("Status Code:", response.status_code)
            print("Response Content:", response.content)
            continue

        try:
            with open("speech.mp3", "wb") as f:
                f.write(response.content)
        except Exception as e:
            print("Error writing file:", e)
            continue

        try:
            pygame.mixer.init()
            pygame.mixer.music.load("speech.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy() == True:
                continue
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except pygame.error as e:
            print("Pygame error:", e)
            break  # Break the loop if there's an error with pygame

# Example usage (replace with your actual robot object):
# robot = YourRobotObject()
# TextToSpeech(robot)


# Example usage (replace with your actual robot object):
# robot = YourRobotObject()
# TextToSpeech(robot)


def TextToSpeech( robot):
    if robot.robot_response.language == "en-US":
        TextToSpeech2(robot)
        return
    speech = gTTS(text=str(robot.robot_response.response.choices[0].message.content), lang=robot.robot_response.language)
    # delete the file if it exist

    if os.path.exists("speech.mp3"):
        os.remove("speech.mp3")
    speech.save("speech.mp3")

    # # change the rate to be faster
    # rate = 1.5
    # data, samplerate = sf.read("speech.mp3")
    # sf.write("speech.mp3", data, int(32000))


    # audio, sr = lr.load("speech.mp3", sr=44100)
    # new_audio = lr.effects.pitch_shift(audio, sr, n_steps=-2)
    # sf.write("speech.mp3", new_audio, sr)    

    pygame.mixer.init()
    pygame.mixer.music.load("speech.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def GenerateResponse(Prompt, UserText, MaxTokens):
    print("Generating response...")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": Prompt},
            {"role": "user", "content": UserText},
        ],
        max_tokens=int(MaxTokens),
        temperature=0.7,
        n = 1
    )
    return completion
