# TripleSumo, 
## a virtual multi-agent RL platform based on OpenAI/Gym and Mujoco. 
![]("https://github.com/niart/triplesumo/blob/5aea698826bd43a1afe0cbc8df33fb350a847333/25_35.gif)

### This game is introduced in publication [Learning Cooperative Behaviours in Adversarial Multi-agent Systems](https://link.springer.com/chapter/10.1007/978-3-031-15908-4_15)([full text](https://drive.google.com/file/d/1gAvAhV5qtRpQqhONvBASjzIKGk6CeWje/view?usp=sharing)).
A live demo of this game can be found in **[This Video](https://www.youtube.com/watch?v=qSSW6TypXdQ&t=100s)**. 
You're welcome to visit the **[author's Youtube page](https://www.youtube.com/@intelligentautonomoussyste5467/videos)** to find more about her work. Contact her at **niwang.cs@gmail.com** if you have inquiry.

This project is an extension of platform [Robosumo](https://github.com/openai/robosumo) with new interfaces. 

Steps of installing triplesumo:
1. Download [Mujoco200](https://www.roboti.us/download.html), rename the package into mujoco200, then extract it in 
   ```/home/your_username/.mujoco/ ```, then download the [license](https://www.roboti.us/license.html) into the same directory
2. Add ```export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/your_username/.mujoco/mujoco200/bin``` to your ```~/.bashrc```, and then ```source ~/.bashrc```
3. Use Anaconda to create a virtual environment 'triple_sumo' with ```conda env create -f triplesumo2021.yml```; Then ```conda activate triple_sumo```.
4. ```git clone https://github.com/niart/triplesumo.git``` and ```cd triplesumo```
5. Use the ```envs``` foler of this repository to replace the ```gym/envs``` installed in your conda environment triplesumo. 
6. To train blue agent in an ongoing game between red and green, run ```cd train_bug```, then```python runmain2.py```. 
7. If you meet error ```Creating window glfw ... ERROR: GLEW initalization error: Missing GL version```, you may add ```export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so``` to ```~/.bashrc```, then ```source ~/.bashrc```. 

key algorithm:

The reward function is in triant.py

The training algorithm is DDPG4.py in "train bug"

If you want to cite this game:
```
@misc{triplesumo,
  howpublished = {Wang, N., Das, G.P., Millard, A.G. (2022). Learning Cooperative Behaviours in Adversarial Multi-agent Systems. In: Pacheco-Gutierrez, S., Cryer, A., Caliskanelli, I., Tugal, H., Skilton, R. (eds) Towards Autonomous Robotic Systems. TAROS 2022. Lecture Notes in Computer Science(), vol 13546. Springer, Cham. https://doi.org/10.1007/978-3-031-15908-4_15} 
```  

An overview of TripleSumo game:

<img src="https://github.com/niart/triplesumo/blob/main/triple.png" width=50% height=50%>

Train the newly added agent with DDPG:

<img src="https://github.com/niart/triplesumo/blob/main/3rewards.png" width=50% height=50%>

Wining rate of the team during training and testing:

<img src="https://github.com/niart/triplesumo/blob/main/hybrid_rate.png" width=50% height=50%>

Steps needed to win:


<img src="https://github.com/niart/triplesumo/blob/main/steps.png" width=50% height=50%>


