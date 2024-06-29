  ###################################### SimplifAI ##########################################
##                                File for HackBCN EVENT                                   ##
##                                     Author: Erwan                                       ##
##                                   Date: 2024-06-29                                      ##
##                                     Version: 1.0                                        ##
##                                Python Version: 3.10.11                                  ##
  ###################################### SimplifAI ##########################################

import numpy as np
import speech_recognition as sr
from Loop import Loop
from Config import ReadKeywords, ReadConfigFile
from Class import InitAudioData, InitRobotBehavior, InitSpeechRecognition, InitRobotResponse, InitRobot, InitUser

def InitBot( KeyWordDesactivate, KeyWordActivate, languages):
    AudioData = InitAudioData()
    robot_behavior = InitRobotBehavior( keywords=["simplify, simplifAI"] , keywords_deactivate= KeyWordDesactivate, keywords_activate= KeyWordActivate)
    recognizer = InitSpeechRecognition()
    robot_response = InitRobotResponse( Languages=languages)
    dictionary = ReadConfigFile("./Config/", "en-US")
    robot = InitRobot( Name="SimplifAI", AudioData=AudioData, RobotBehavior=robot_behavior, SpeechRecognition=recognizer, RobotResponse=robot_response, dictionary=dictionary)
    return robot

def Bot():
    KeyWordActivate, KeyWordDesactivate, languages = ReadKeywords( "./Config/") 
    robot = InitBot( KeyWordDesactivate, KeyWordActivate, languages)
    user = InitUser( Name="User", Language="en-US", Transcription="", Emotion="")
    robot = Loop(robot, user)
    return robot

if __name__ == "__main__":
    Bot()