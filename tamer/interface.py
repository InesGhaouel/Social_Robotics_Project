import os
import pygame
import pyaudio
import wave
import speech_recognition as sr
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

class Interface:
    """ Pygame interface for training TAMER """

    def __init__(self, action_map):
        self.action_map = action_map
        pygame.init()
        self.font = pygame.font.Font("freesansbold.ttf", 32)

        # set position of pygame window (so it doesn't overlap with gym)
        os.environ["SDL_VIDEO_WINDOW_POS"] = "1000,100"
        os.environ["SDL_VIDEO_CENTERED"] = "0"

        self.screen = pygame.display.set_mode((200, 100))
        area = self.screen.fill((0, 0, 0))
        pygame.display.update(area)

    def get_scalar_feedback(self):
        """
        Get human input. 'W' key for positive, 'A' key for negative.
        Returns: scalar reward (1 for positive, -1 for negative)
        """
        reward = 0
        area = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_w:    #sAY IF IT4S GOOD 
                    area = self.screen.fill((0, 255, 0))
                    reward = +1
                    
                    break
                elif event.key == pygame.K_a:  #BAD FEED BACK
                    area = self.screen.fill((255, 0, 0))
                    reward = -1
                    break
                #el
                
                elif event.key == pygame.K_l :   #gOP LEFT
                    area = self.screen.fill((255, 0, 0))
                    reward= +2

                    break
                elif event.key == pygame.K_d:  #GO RIGHT 
                    area = self.screen.fill((2, 255, 0)) 
                    reward = +3
                    break
        pygame.display.update(area)
        return reward
    
    def get_sound(self):
        # the file name output you want to record into
        filename = "recorded.wav"
        # set the chunk size of 1024 samples
        chunk = 1024
        # sample format
        FORMAT = pyaudio.paInt16
        # mono, change to 2 if you want stereo
        channels = 1
        # 44100 samples per second
        sample_rate = 44100
        record_seconds = 3
        # initialize PyAudio object
        p = pyaudio.PyAudio()
        # open stream object as input & output
        stream = p.open(format=FORMAT,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk)
        frames = []
        print("\n Recording...")
        for i in range(int(44100 / chunk * record_seconds)):
            data = stream.read(chunk)
            # if you want to hear your voice while recording
            # stream.write(data)
            frames.append(data)
        print("\n Finished recording.")
        # stop and close stream
        stream.stop_stream()
        stream.close()
        # terminate pyaudio object
        p.terminate()
        # save audio file
        # open the file in 'write bytes' mode
        wf = wave.open(filename, "wb")
        # set the channels
        wf.setnchannels(channels)
        # set the sample format
        wf.setsampwidth(p.get_sample_size(FORMAT))
        # set the sample rate
        wf.setframerate(sample_rate)
        # write the frames as bytes
        wf.writeframes(b"".join(frames))
        # close the file
        wf.close()
        r = sr.Recognizer()
        with sr.AudioFile("recorded.wav") as source:
            audio_text = r.listen(source)
            
            text = r.recognize_google(audio_text)
            print(text)
            return text

    def get_speech_feedback(self):
        
        
        area = None
        text=self.get_sound()
            
        if text=="yes":  #Good feedback
            
            area = self.screen.fill((0, 255, 0))
            reward = +1

        elif text=='no': #Bad feed back
            area = self.screen.fill((255, 0, 0))
            reward = -1

        if text== "back" :   #gO LEFT
            area = self.screen.fill((255, 0, 0))
            reward = +2 

        elif text=="forward":  #GO RIGHT 
            area = self.screen.fill((2, 255, 0)) 
            reward = +3

        pygame.display.update(area)

        return reward

    #Gestures Part :
    def get_gest(self):
        # TechVidvan hand Gesture Recognizer


        
        # initialize mediapipe
        mpHands = mp.solutions.hands
        hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mpDraw = mp.solutions.drawing_utils

        # Load the gesture recognizer model
        model = load_model('mp_hand_gesture')

        # Load class names
        f = open('gesture.names', 'r')
        classNames = f.read().split('\n')
        f.close()
        print(classNames)


        # Initialize the webcam
        cap = cv2.VideoCapture(0)

        while True:
            # Read each frame from the webcam
            _, frame = cap.read()

            x, y, c = frame.shape

            # Flip the frame vertically
            frame = cv2.flip(frame, 1)
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get hand landmark prediction
            result = hands.process(framergb)

            
            className = ''

            # post process the result
            if result.multi_hand_landmarks:
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    for lm in handslms.landmark:
                        # print(id, lm)
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)

                        landmarks.append([lmx, lmy])

                    # Drawing landmarks on frames
                    mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                    # Predict gesture
                    prediction = model.predict([landmarks])
                    # print(prediction)
                    classID = np.argmax(prediction)
                    className = classNames[classID]
                    print(className)

            # show the prediction on the frame
            cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,0,255), 2, cv2.LINE_AA)
            print("CLass Name ",className)
            # Show the final output
            cv2.imshow("Output", frame) 

 
        
            return className

    def get_gestures_feedback(self):
        
        reward = 0
        area = None
        for event in pygame.event.get():
            text=self.get_gest()
            print(text)
            #if event.type == pygame.KEYDOWN:
                
            if text=="thumbs up":  #Good Feedback
                area = self.screen.fill((0, 255, 0))
                reward = 1
                print("+1")
                break
            elif text=='thumbs down':   #Bad Feed Back
                area = self.screen.fill((255, 0, 0))
                reward = -1
                break
            elif text=='okay':   #Go left
                area = self.screen.fill((255,0,0))
                reward = +2
                break
            elif text=='fist':    #Go right

                area = self.screen.fill((255,0,0))
                reward = +3
                break
        pygame.display.update(area)

        return reward   




    def show_action(self, action):
        """
        Show agent's action on pygame screen
        Args:
            action: numerical action (for MountainCar environment only currently)
        """
        area = self.screen.fill((0, 0, 0))
        pygame.display.update(area)
        text = self.font.render(self.action_map[action], True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (100, 50)
        area = self.screen.blit(text, text_rect)
        pygame.display.update(area)
