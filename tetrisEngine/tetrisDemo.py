from tetrisEnv import *
from tetrisAgent import *
from featureExtractor import *
from RLtoolkit.RLinterface import RLinterface
import numpy


# numpy.set_printoptions(threshold='nan')


def main():
    envconf = {
        'BOARDWIDTH': 10,
        'BOARDHEIGHT': 20,
        'FPS': 10
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
    episode = rli.episodes(5)
    print "episode"
    print episode


if __name__ == '__main__':
    main()
