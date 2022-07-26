TripleSumo, a virtual multi-agent RL platform
Learning cooperative behaviours in adversarial multi-agent systems
This project is an extension of platform "Robosumo" (https://github.com/openai/robosumo) with new interfaces. 

Dependencies: python==3.7, Gym==10.2, Mujoco>=2.0
After you install gym, please replace folder "gym" with the folder "gym" on this repository. 
Clone the folder "train bug" onto your local PC, cd into it, and "python runmain2.py"

key algorithm:
The reward function is in triant.py
The training algorithm is DDPG4.py in "train bug"

![](https://github.com/niart/triplesumo_TAROS/blob/main/25_35.gif)

An overview of TripleSumo game:

<img src="https://github.com/niart/triplesumo/blob/main/triple.png" width=50% height=50%>

Train the newly added agent with DDPG:

<img src="https://github.com/niart/triplesumo/blob/main/3rewards.png" width=50% height=50%>

Wining rate of the team during training and testing:

<img src="https://github.com/niart/triplesumo/blob/main/hybrid_rate.png" width=50% height=50%>

Steps needed to win:


<img src="https://github.com/niart/triplesumo/blob/main/steps.png" width=50% height=50%>


