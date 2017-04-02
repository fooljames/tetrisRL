from tetrisEnv import *
from tetrisAgent import *
from featureExtractor import *
from RLtoolkit.RLinterface import RLinterface
import numpy


# numpy.set_printoptions(threshold='nan')

#TODO
"""
-2. no reward.. weight should not updated
-1. check inf issue with weights
 0. Make sure get next state really works..
 1. All features to be correct..
 2. Different shape get their own feature set (One hot encoding)
 3. Save weights every epoch
 5. Normalize features (0 - 1)
"""


def main():
    envconf = {
        'BOARDWIDTH': 10,
        'BOARDHEIGHT': 20,
        'FPS': 100
    }

    agentConf = {
        'gamma': 0.3,
        'alpha': 1.0,
        'epsilon': 0.2,
        'featureExtractor': SimpleFeatureExtractor()
    }

    env = TetrisEnv(envconf)
    agent = QLearningApproxAgent(env, agentConf)
    rli = RLinterface(agent.agentFn, env.envFn)
    # run two episodes of tetris and print state, action, reward for every step
    episode = rli.episodes(30)
    print "episode"
    print episode


if __name__ == '__main__':
    main()
