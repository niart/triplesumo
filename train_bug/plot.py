import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
sns.set_style()


def get_data():
    ddpg1 = pd.read_excel('./1w_5apr_vel_ddpg.xlsx')
    #print(type(ddpg1.con1))
    ddpg1 = ddpg1.con1.rolling(500).mean()

    return ddpg1


data = get_data()
ax = sns.lineplot(data=data, dashes=False)

plt.xlabel("Episode")
plt.ylabel("Rewards")
plt.title("28_vel_Ant VS Ant VS Ant")
# plt.show()
plt.savefig('12_march_vel')

