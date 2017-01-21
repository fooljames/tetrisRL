from tetrisEnv import *
from tetrisAgent import *
from RLtoolkit.RLinterface import RLinterface
import numpy


# numpy.set_printoptions(threshold='nan')


def main():
    envconf = {
        'BOARDWIDTH': 10,
        'BOARDHEIGHT': 20,
        'FPS': 10
        }

    env = TetrisEnv(envconf)
    agent = RandomAgent(env)
    rli = RLinterface(agent.agentFn, env.envFn)
    # run two episodes of tetris and print state, action, reward for every step
    episode = rli.episodes(1)
    print episode


if __name__ == '__main__':
    main()
