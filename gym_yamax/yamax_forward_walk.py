from gym_yamax.forward_walker import ForwardWalker
from roboschool.gym_urdf_robot_env import RoboschoolUrdfEnv
from roboschool.scene_abstract import cpp_household
from roboschool.scene_stadium import SinglePlayerStadiumScene
import numpy as np


class RoboschoolYamaXForwardWalk(ForwardWalker, RoboschoolUrdfEnv):
    random_yaw = False
    foot_list = ["foot_right", "foot_left"]
    right_leg = "leg_right_2"
    left_leg = "leg_left_2"
    hip_part = "hip"
    num_joints = 14

    def __init__(self):
        ForwardWalker.__init__(self)
        RoboschoolUrdfEnv.__init__(self,
                                   "robot_models/yamax.urdf",
                                   "body",
                                   action_dim=self.num_joints, obs_dim=self.num_joints + 3,
                                   fixed_base=False,
                                   self_collision=True)

    def create_single_player_scene(self):
        # 8 instead of 4 here
        return SinglePlayerStadiumScene(gravity=9.8, timestep=0.0165/8, frame_skip=8)

    def robot_specific_reset(self):
        ForwardWalker.robot_specific_reset(self)
        self.set_initial_orientation(yaw_center=0, yaw_random_spread=np.pi)
        self.head = self.parts["head"]

    random_yaw = False

    def set_initial_orientation(self, yaw_center, yaw_random_spread):
        self.cpp_robot.query_position()
        if not self.random_yaw:
            yaw = yaw_center
        else:
            yaw = yaw_center + \
                self.np_random.uniform(
                    low=-yaw_random_spread, high=yaw_random_spread)

        self.initial_z = - self.cpp_robot.root_part.pose().xyz()[2] + 0.01

        cpose = cpp_household.Pose()
        cpose.set_xyz(self.start_pos_x, self.start_pos_y,
                      self.initial_z)
        # just face random direction, but stay straight otherwise
        cpose.set_rpy(0, 0, yaw)
        self.cpp_robot.set_pose_and_speed(cpose, 0, 0, 0)
