  ###################################### SimplifAI ##########################################
##                                File for HackBCN EVENT                                   ##
##                                     Author: Erwan                                       ##
##                                   Date: 2024-06-29                                      ##
##                                     Version: 1.0                                        ##
##                                Python Version: 3.10.11                                  ##
  ###################################### SimplifAI ##########################################

import openai
import numpy as np
import soundfile as sf
import pygame

from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import speech_recognition as sr
from Listener import ListenerOff
from TurnOff import CheckTurnOff, TurnOffRobot
from GenerateResponse import GenerateResponse, TextToSpeech
import gtts
import time
from Config import FillDictionary, ModifyRow, ReadConfigFile, DisplayDictionary

def KeywordNeeded( transcription, keywords):
    if "hello" in transcription or "Hello" in transcription or "HELLO" in transcription or "hi" in transcription or "Hi" in transcription or "HI" in transcription or "hey" in transcription or "Hey" in transcription or "HEY" in transcription or "bonjour" in transcription or "Bonjour" in transcription or "BONJOUR" in transcription or "holà" in transcription or "Holà" in transcription or "HOLÀ" in transcription or "hola" in transcription or "Hola" in transcription or "HOLA" in transcription:
        return True
    return False

def CreatePrompt( robot , user):
    robot.dictionnary = ReadConfigFile("./Config/", robot.robot_response.language)
        
    robot.robot_response.prompt = "Context: " + str(robot.dictionary["Context"]) + "\n" + "Language: " + str(robot.robot_response.language) + "\n" + "Prompt: " + str(robot.dictionnary["Prompt"]) + "\n" + "Answer: "
    print("Prompt created")
    userText =  "Question/sentence: " + str(user.transcription) + "\n" + "Answer: "

    print("Prompt is : " + robot.robot_response.prompt)
    return robot.robot_response.prompt , userText

def Loop(robot, user):
    while True:
        print("Waiting...")
        while True:
            if robot.robot_behavior.keyword_needed:
                user.transcription, robot.robot_response.language, robot.robot_behavior.spoken, robot.dictionnary = ListenerOff(robot)
                user.language = robot.robot_response.language
                print("Language is " + robot.robot_response.language)
            if robot.robot_behavior.spoken:
                robot.robot_behavior.active = KeywordNeeded(user.transcription, robot.robot_behavior.keywords)
                if robot.robot_behavior.active and robot.robot_behavior.keyword_needed:
                    robot.robot_behavior.keyword_needed = False
                if robot.robot_behavior.keyword_needed == False:
                    reconizer = sr.Recognizer()
                    micro = sr.Microphone()
                    with micro as source:
                        pygame.mixer.init()
                        pygame.mixer.music.load("beep.mp3")
                        pygame.mixer.music.play()

                        reconizer.adjust_for_ambient_noise(source)
                        audio = reconizer.listen(source)
                    try:
                        user.transcription = reconizer.recognize_google(audio, language=user.language)
                        print ("You said: " + user.transcription)
                        break
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                        continue
                    except sr.RequestError:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
                        continue
        
        robot.robot_response.prompt, userText = CreatePrompt(robot, user)

        if CheckTurnOff( robot , user) == True:
            robot = TurnOffRobot(robot, user, robot.dictionnary)
            continue
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print("Prompt is : " + robot.robot_response.prompt)
        with open("prompt.txt", "a") as f:
            f.truncate(0)
            f.write(str(robot.robot_response.prompt))
            f.write("\n")
            f.close()
        
        robot.robot_response.response = GenerateResponse( robot.robot_response.prompt, userText, robot.dictionnary["MaxTokens"])
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open("response.txt", "a") as f:
            f.truncate(0)
            f.write(str(robot.robot_response.response.choices[0].message.content))
            f.write("\n")
            f.close()
        # AddSentence( Language=robot.robot_response.language, Name="SimplifAI", Value=str(robot.robot_response.response.choices[0].message.content), Date=date, nb=nb)
        TextToSpeech(robot)

    return robot