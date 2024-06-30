  ###################################### SimplifAI ##########################################
##                                File for HackBCN EVENT                                   ##
##                                     Author: Erwan                                       ##
##                                   Date: 2024-06-29                                      ##
##                                     Version: 1.0                                        ##
##                                Python Version: 3.10.11                                  ##
  ###################################### SimplifAI ##########################################

import numpy as np
import soundfile as sf

from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import speech_recognition as sr
from Config import FillDictionary, ModifyRow, ReadConfigFile, DisplayDictionary

def GetLanguage( transcription, keywords, language ):
    # keywords is a dict[language][word]
    for word in keywords[language]:
        print("word: " + word)
        print ("transcription: " + transcription)
        if word.lower() in transcription.lower():
            return True, language
    return False, ""

def ListenerOff(robot):
    with robot.audio_data.microphone as source:
        robot.audio_data.recognizer.adjust_for_ambient_noise(source)
        audio = robot.audio_data.recognizer.listen(source)
        try:
            for language in robot.robot_response.languages:
                transcription = robot.audio_data.recognizer.recognize_google(audio, language=language)
                spoke, language = GetLanguage(transcription, robot.robot_behavior.keywords_activate, language)
                if spoke and language != "":
                    dictionary = ReadConfigFile("./Config/", language )
                    return transcription, language , True, dictionary
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "", "", False, ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return "", "", False, ""
    
    return "", "", False, ""

def ListenerOn( recognizer, microphone, language):
    rec = sr.Recognizer()
    micro = sr.Microphone()
    with micro as source:
        rec.adjust_for_ambient_noise(source)
        audio = rec.listen(source)
        try:
            transcription = rec.recognize_google(audio, language)
            return transcription, True
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "" , False
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return "" , False
