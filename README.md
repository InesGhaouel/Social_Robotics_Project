# Social_Robotics_Project
The purpose of this project is to integrate a human feedback into an agent's learning .

We first did a benchmark of similar existing projects :


Then we chose to implement  the TAMER algorithm from "Interactively Shaping Agents via Human Reinforcement" (Knox, Stone - 2009)

We replicate this project by adding two ways for the user to give a feedback.
The first one is by speech : "yes" or "no","back" and "forward" using Speech to text file (recording then reading then return the text ).
The second one is by hand gestures : "Thumbs up" or "Thumbs down" , "fist" and "smile" .
The model is already trained using the method descriptive+ evaluative.
If you wan to train it yourself uncomment the lines 41 and 43 in the run.py file and comment the line 39 .


the installations can be installed using the line :

pip install -r requirements.txt
