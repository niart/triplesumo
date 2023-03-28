## This version is to train single agent with velocity. has [0], but No wining rate
import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env
from mujoco_py import functions
import mujoco_py

class TriantplusEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    #state = np.zeros(shape=15, dtype = float32)
    def __init__(self):
        self.state = np.zeros(shape=19, dtype=np.float32)
        self.vel = np.zeros(shape=19, dtype=np.float32)

        self.mapping = {
        "torso_geom": 0, "aux_1_geom":1, "front_left_leg_geom":2,
        "front_left_ankle_geom":3, "aux_2_geom":4, "front_right_leg_geom":5,
        "front_right_ankle_geom":6, "aux_3_geom":7, "back_left_leg_geom":8,
        "back_left_ankle_geom":9, "aux_4_geom":10, "back_right_leg_geom":11,
        "back_right_ankle_geom":12,
           
        "torso_geom2":13, "aux_1_geom2":14, "front_left_leg_geom2": 15,
         "front_left_ankle_geom2": 16, "aux_2_geom2": 17, "front_right_leg_geom2": 18,
         "front_right_ankle_geom2": 19, "aux_3_geom2": 20, "back_left_leg_geom2": 21,
         "back_left_ankle_geom2": 22, "aux_4_geom2": 23, "back_right_leg_geom2": 24,
         "back_right_ankle_geom2": 25,
         
         "torso_geom3": 26, "aux_1_geom3": 27, "front_left_leg_geom3": 28,
         "front_left_ankle_geom3": 29, "aux_2_geom3": 30, "front_right_leg_geom3": 31,
         "front_right_ankle_geom3": 32, "aux_3_geom3": 33, "back_left_leg_geom3": 34,
         "back_left_ankle_geom3": 35, "aux_4_geom3": 36, "back_right_leg_geom3": 37,
         "back_right_ankle_geom3": 38, 
         
         "tatami": 39, "rightborder": 40,
         "leftborder":41, "topborder": 42, "bottomborder": 43, "floor": 44
         }

        mujoco_env.MujocoEnv.__init__(self, "./tatami.xml", 5)
        utils.EzPickle.__init__(self)

    def step(self, action):
        self.do_simulation(action, 5)
        done = False
        self.score = 0
        sparse_reward = 0
        reward = 0

        #reward
        index_ant = self.model.body_name2id("torso")
        self.ant_pos = self.sim.data.body_xpos[index_ant]
        self.ant_vel = self.sim.data.body_xvelp[index_ant] 
        
        index_bug = self.model.body_name2id("torso2")
        self.bug_pos = self.sim.data.body_xpos[index_bug]
        self.bug_vel = self.sim.data.body_xvelp[index_bug] 
        
        index_spider = self.model.body_name2id("torso3")
        self.spider_pos = self.sim.data.body_xpos[index_spider]
        self.spider_vel = self.sim.data.body_xvelp[index_spider] 
        
        # middle: ant
        # small: bug  [8:16]
        # big: spider

        ## Bug attacks spider
        # spider >= bug
        if self.spider_pos[0:1] >= self.bug_pos[0:1]:
            x_reward = self.spider_vel[0:1] + self.bug_vel[0:1] 
          
            # spider < bug
        else:  
            x_reward = - self.spider_vel[0:1] - self.bug_vel[0:1]
          
        # y       
        # spider >= bug
        if self.spider_pos[1:2] >= self.bug_pos[1:2]:
            y_reward = self.spider_vel[1:2] + self.bug_vel[1:2] 
           
        # spider < bug
        else:    
            y_reward = - self.spider_vel[1:2] - self.bug_vel[1:2]
            
        self_opponent_reward = x_reward + y_reward

        #partner_reward
        # ant >= spider
        if self.ant_pos[0:1] >= self.spider_pos[0:1]:
            partner_x_reward = - self.ant_vel[0:1] 
 
        # ant < spider
        else:    
            partner_x_reward = self.ant_vel[0:1]
 
        # y       
        # ant >= spider 
        if self.ant_pos[1:2] >= self.spider_pos[1:2]:
            partner_y_reward = - self.ant_vel[1:2] 
 
        # ant < spider
        else:    
            partner_y_reward = self.ant_vel[1:2]

        partner_reward = partner_x_reward + partner_y_reward

        reward = 5 * self_opponent_reward + 5 * partner_reward - 4
        
        done = self.isout(self.ant_pos) or self.isout(self.spider_pos) or self.isout(self.bug_pos)  #距离超出，即结束

        if done:        
            if self.isout(self.spider_pos): 
                reward += 500
                sparse_reward = 500
                self.score = 1
                print("The team wins!!!!!!!!!!!!!!!!!!!!!!")      
            elif self.isout(self.ant_pos) or self.isout(self.bug_pos):
                reward -= 400
                sparse_reward = -400
                self.score = -1
                print("The team loses!!!!!!!!!!!!!!!!!!!!!!")
        ob = self._get_obs()  #观测值，在下面
        return ob, self.score, done, {} # sparse_reward
        
    def isout(self, agent):
        for i in agent:
            if i > 2:
                return True
            elif i < -2:
                return True
        return False


    def _get_obs(self):
        retn_obv = np.concatenate((
            [self.score],
            # mass center position
            self.ant_pos.flat,
            self.bug_pos.flat,
            self.spider_pos.flat,
            # mass center velocity
            self.ant_vel.flat,
            self.bug_vel.flat,
            self.spider_vel.flat,

            # contact_forces
            self.link_force().flat,

            # 3-dim position and velocity
            self.sim.data.qpos.flat[0:],
            self.sim.data.qvel.flat[0:],

        ))
        return retn_obv

        #获取6-aixs接触力
    def link_force(self):
        force = np.zeros(shape=(45,6), dtype = np.float64)
        for i in range(self.sim.data.ncon):
            contact = self.sim.data.contact[i]
            c_array = np.zeros(6, dtype=np.float64)
            functions.mj_contactForce(self.sim.model, self.sim.data, i, c_array)
            force[self.mapping[self.sim.model.geom_id2name(contact.geom1)]] = c_array[:6]
            force[self.mapping[self.sim.model.geom_id2name(contact.geom2)]] = c_array[:6]
        return force[:39].flat.copy()

    def reset_model(self):
        qpos = self.init_qpos
        qvel = self.init_qvel
        self.set_state(qpos, qvel)
        return self._get_obs()

        #摄像机视角
    def viewer_setup(self):
        if self.viewer is not None:
            self.viewer._run_speed = 0.5
            self.viewer.cam.trackbodyid = 0
            # self.viewer.cam.lookat[2] += .8
            self.viewer.cam.elevation = -25
            self.viewer.cam.type = 1
            self.sim.forward()
            self.viewer.cam.distance = self.model.stat.extent * 1.0
        # Make sure that the offscreen context has the same camera setup
        if self.sim._render_context_offscreen is not None:
            self.sim._render_context_offscreen.cam.trackbodyid = 0
            # self.sim._render_context_offscreen.cam.lookat[2] += .8
            self.sim._render_context_offscreen.cam.elevation = -25
            self.sim._render_context_offscreen.cam.type = 1
            self.sim._render_context_offscreen.cam.distance = \
                self.model.stat.extent * 1.0
        self.buffer_size = (1280, 800)

