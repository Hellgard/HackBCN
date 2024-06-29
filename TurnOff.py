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
from GenerateResponse import GenerateResponse, TextToSpeech

def CheckTurnOff( robot, user):
    for word in robot.robot_behavior.keywords_deactivate[user.language]:
        print("Checking if " + word + " is in " + user.transcription)
        if word in user.transcription:
            return True
    return False

def SayGoobye( robot, user, dictionary):
    robot.robot_response.response = GenerateResponse(robot.robot_response.prompt, dictionary["MaxTokens"])
    TextToSpeech(robot)

def TurnOffRobot(robot , user, dictionary):
    robot.robot_behavior.active = False
    robot.robot_behavior.keyword_needed = True
    print("Robot is now inactive")
    SayGoobye(robot, user, dictionary)
    return robot
