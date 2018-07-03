# Chair_The_Fed_Rl

Using Reinforcement learning to play Chair The Fed.

# About the Game:
Chair the Fed designed by Federal Reserve Bank of San Francisco to teach about the effect of external factors like news and how by manipulating the fed funds rate, you can keep the inflation and unemployment at target rates.
The game puts the player in the role of setting monetary policy as Chair of the Fed for fifteen quarters. The goals are as follows:
inflation (2 percent) and unemployment (5 percent) and the information in the headline reflects changes in the levels of inflation and unemployment. Fed funds rate is the primary tool for monetary policy and is shown on the game screen.

![alt text](https://github.com/lucky630/Chair_The_Fed_Rl/blob/master/record/hh0.PNG)

The game ends on an announcement screen indicating "Congratulations" if the Chair has kept the economy on track (close to the goals for inflation and unemployment) or "Sorry" if the goals have not been met.

![alt text](https://github.com/lucky630/Chair_The_Fed_Rl/blob/master/record/both.png)

[Link to Game](https://sffed-education.org/chairthefed/WebGamePlay.html)

# Architecture

![alt text](https://github.com/lucky630/Chair_The_Fed_Rl/blob/master/record/arch_diag.jpg)

# Video

# Setup Requirements
- Pytesseract
- Tensorflow
- Keras
- MatplotLib
- selenium
- PIL
- cv2
- torch

# To Run
Run main.py in train or test mode. Toggle the train_mode variable to run in train or test mode.

# To Do list-
1. there is too much up and down fed rates are set by the agent have to find a policy which having very low fluctuation.
2. need to run the model for more number of epochs.
3. loss value is not changing from one epoch to other need to check that.
