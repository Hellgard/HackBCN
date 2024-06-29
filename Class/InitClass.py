  ###################################### SimplifAI ##########################################
##                                  File for Init Class                                    ##
##                                     Author: Erwan                                       ##
##                                   Date: 2023-03-20                                      ##
##                                     Version: 1.0                                        ##
##                                Python Version: 3.10.6                                   ##
  ###################################### SimplifAI ##########################################

from Class import *

def InitAudioData( language):
    channels = 1
    rate = 44100
    chunk_size = 1024
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    record_seconds = 3
    return AudioData(channels, rate, chunk_size, record_seconds, language, microphone, recognizer)

def InitRobotBehavior(keywords):
    keyword_needed = True
    return RobotBehavior(keyword_needed, keywords)

def InitSpeechRecognition():
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    return SpeechRecognition(tokenizer, model)

def InitRobotResponse( RobotDescription, Response, Language, Prompt):
    robot_description = RobotDescription
    Response = Response
    Prompt = Prompt
    language = Language
    return RobotResponse(robot_description, Response, language)

def InitRobot( Name, AudioData, RobotBehavior, SpeechRecognition, RobotResponse, dictionary):
    name = Name
    dictionary = dictionary
    audio_data = AudioData
    robot_behavior = RobotBehavior
    speech_recognition = SpeechRecognition
    robot_response = RobotResponse
    return Robot(name, audio_data, robot_behavior, speech_recognition, robot_response)

def InitRobotClass( language, keywords, RobotDescription, Transcription, Language, Name):
    audio_data = InitAudioData(language)
    robot_behavior = InitRobotBehavior(keywords)
    speech_recognition = InitSpeechRecognition()
    robot_response = InitRobotResponse(RobotDescription, Transcription, Language)
    robot = InitRobot(Name, audio_data, robot_behavior, speech_recognition, robot_response)
    return robot

def InitUser( Name, Language, Emotion):
    name = Name
    language = Language
    emotion = Emotion
    return User(name, language )

def InitUsers( users):
    return Users(users)
