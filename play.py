
#add parent dir to find package. Only needed for source code build, pip install doesn't need it.
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from argparse import ArgumentParser

from yamaxenv import YamaXEnv

from baselines.ppo1 import mlp_policy
from baselines.common import tf_util as U

from baselines import logger

import tensorflow as tf

def main(iteration, challenge, modelpath):
    logger.configure()
    sess = U.make_session()
    sess.__enter__()

    env = YamaXEnv(logfile="log.csv", renders=True)
    def policy_fn(name, ob_space, ac_space):
        return mlp_policy.MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space,
            hid_size=64, num_hid_layers=2)

    obs = env.reset()
    pi = policy_fn('pi', env.observation_space, env.action_space)
    tf.train.Saver().restore(sess, modelpath)
    for i in range(iteration):
        print("Iteration {} started".format(i))
        if not challenge:
            obs = env.reset()
        done = False
        while not done:
            action = pi.act(True, obs)[0]
            obs, reward, done, info = env.step(action)
            env.render()
            if challenge and reward == -1:
                break


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--iter', type=int, default=1)
    parser.add_argument('--model', type=str, default='model/deepl2_10000000')
    parser.add_argument("--challenge", action="store_true")
    args = parser.parse_args()
    main(args.iter, args.challenge, args.model)
