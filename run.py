"""
Implementation of TAMER (Knox + Stone, 2009)
When training, use 'W' and 'A' keys for positive and negative rewards
"""

import asyncio
import gym
import matplotlib.pyplot as plt
from tamer.agent import Tamer
import numpy as np
avg=[]
truc=[]
o=[]
async def main():
    env = gym.make('MountainCar-v0')

    # hyperparameters
    
    discount_factor = 1
    epsilon = 0  # vanilla Q learning actually works well with no random exploration
    min_eps = 0
    num_episodes = 2
    tame = True  # set to false for vanilla Q learning

    #Ask the user which channel he wants to use to give his information 
    choice=int(input("Tap 0 for keyboard return, 1 for speech recognition or 2 for gestures recognition \n"))
    if choice == 0 :
        print("You chose the keyboard ")
    elif choice == 1 :
        print("You chose Speech recognition")
    elif choice == 2 : 
        print(" You chose Gestures Recognition ")
    # set a timestep for training TAMER
    # the more time per step, the easier for the human
    # but the longer it takes to train (in real time)
    # 0.2 seconds is fast but doable
    tamer_training_timestep = 0.2

    agent = Tamer(env,choice, num_episodes, discount_factor, epsilon, min_eps, tame,
                  tamer_training_timestep, model_file_to_load="autosave")
    #agent = Tamer(env,choice, num_episodes, discount_factor, epsilon, min_eps, tame,
                  tamer_training_timestep, model_file_to_load=None)
    #await agent.train(model_file_to_save='autosave')
    agent.play(n_episodes=20, render=False)

    avg_reward=agent.evaluate(n_episodes=20)
    print("The average reward over 20 episodes is :",avg_reward)




if __name__ == '__main__':
#    for i in range (len(30)):
    asyncio.run(main())





