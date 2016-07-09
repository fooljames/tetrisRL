from tetrisEnv import *
from tetrisAgent import *
from RLtoolkit.RLinterface import RLinterface
import numpy


# numpy.set_printoptions(threshold='nan')


def main():
    envconf = {
        'BOARDWIDTH': 10,
        'BOARDHEIGHT': 20,
        'FPS': 100
        }

    env = TetrisEnv(envconf)
    agent = RandomAgent()
    rli = RLinterface(agent.agentFn, env.envFn)
    # run two episodes of tetris and print state, action, reward for every step
    episode = rli.episodes(3)
    print episode


if __name__ == '__main__':
    main()
