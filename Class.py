  ###################################### SimplifAI ##########################################
##                                File for HackBCN EVENT                                   ##
##                                     Author: Erwan                                       ##
##                                   Date: 2024-06-29                                      ##
##                                     Version: 1.0                                        ##
##                                Python Version: 3.10.11                                  ##
  ###################################### SimplifAI ##########################################

import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import speech_recognition as sr

class AudioData:
    def __init__(self, channels, rate, chunk_size, microphone, recognizer):
        self.channels = channels
        self.rate = rate
        self.chunk_size = chunk_size
        self.microphone = microphone
        self.recognizer = recognizer

class RobotBehavior:
    def __init__(self, keyword_needed, keywords = [], keywords_activate =[], keywords_deactivate = []):
        self.keyword_needed = keyword_needed
        self.active = False
        spoken = False
        self.keywords = keywords
        self.keywords_activate = keywords_activate
        self.keywords_deactivate = keywords_deactivate
        
class SpeechRecognition:
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

class RobotResponse:
    def __init__(self, robot_description, language, response, Prompt, languages):
        self.robot_description = robot_description
        self.response = response
        self.prompt = Prompt
        self.languages = languages
        self.language = language

class Robot:
    def __init__(self, name, audio_data, robot_behavior, speech_recognition, robot_response, dict):
        self.name = name
        self.dictionary = dict
        self.audio_data = audio_data
        self.robot_behavior = robot_behavior
        self.speech_recognition = speech_recognition
        self.robot_response = robot_response

class User:
    def __init__(self, name, language, transcription = "", emotion = ""):
        self.name = name
        self.language = language
        self.transcription = transcription
        self.emotion = emotion

class Users:
    def __init__(self, users):
        number_of_users = len(users)
        self.users = users

def InitAudioData():
    channels = 1
    rate = 44100
    chunk_size = 1024
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    return AudioData(channels, rate, chunk_size, microphone, recognizer)

def InitRobotBehavior(keywords = [], keywords_deactivate = [], keywords_activate = []):
    keyword_needed = True
    return RobotBehavior(keyword_needed, keywords, keywords_activate,keywords_deactivate)

def InitSpeechRecognition():
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    return SpeechRecognition(tokenizer, model)

def InitRobotResponse( RobotDescription="Bonjour, je suis simplifAI, le bot internet qui va changer votre vie", Language="en-US" ,Response = "", Prompt = "", Languages = ["fr-FR", "en-US"]):
    robot_description = RobotDescription
    Response = Response
    Prompt = Prompt
    language = Language
    languages = Languages
    return RobotResponse(robot_description, language, Response, Prompt, languages)

def InitRobot( Name, AudioData, RobotBehavior, SpeechRecognition, RobotResponse, dictionary):
    name = Name
    dictionary = dictionary
    audio_data = AudioData
    robot_behavior = RobotBehavior
    speech_recognition = SpeechRecognition
    robot_response = RobotResponse
    return Robot(name=name, audio_data=audio_data, robot_behavior=robot_behavior, speech_recognition=speech_recognition, robot_response=robot_response, dict=dictionary)

def InitRobotClass( language, keywords, RobotDescription, Transcription, Language, Name):
    audio_data = InitAudioData(language)
    robot_behavior = InitRobotBehavior(keywords)
    speech_recognition = InitSpeechRecognition()
    robot_response = InitRobotResponse(RobotDescription, Transcription, Language)
    robot = InitRobot(Name, audio_data, robot_behavior, speech_recognition, robot_response)
    return robot

def InitUser( Name, Language, Emotion, Transcription):
    name = Name
    language = Language
    emotion = Emotion
    transcription = Transcription
    return User(name, language ,transcription, emotion)

def InitUsers( users):
    return Users(users)
