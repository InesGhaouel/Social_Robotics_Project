# Social_Robotics_Project
The purpose of this project is to integrate a human feedback into an agent's learning .

We first did a benchmark of similar existing projects :
Then we chose to implement  the TAMER algorithm from "Interactively Shaping Agents via Human Reinforcement" (Knox, Stone - 2009)

We replicate this project by adding two ways for the user to give a feedback.
The first one is by speech : "yes" or "no" using Speech to text file (recording then reading then return the text ).
The second one is by hand gestures : "Thumbs up" or "Thumbs down" (folder)

Then We tried two other approaches :
Descriptive learning, Giving only an action an dnot an evaluation anymore :
Speech :  "back" or "forward"
Gestures : "Okay" or "fist"
for left and right respectfully.
The libraries can be installed using the line :

pip install -r requirements.txt
