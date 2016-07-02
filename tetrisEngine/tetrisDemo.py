from tetrisEnv import *
from tetrisAgent import *
from RLtoolkit.RLinterface import RLinterface
import numpy
numpy.set_printoptions(threshold='nan')


def main():
    env = TetrisEnv()
    agent = TetrisAgent()
    rli = RLinterface(agent.tetrisAgent, env.tetris_env)
    # run two episodes of tetris and print state, action, reward for every step
    episode = rli.episodes(1)
    print episode[2]
    print episode[3].shape


if __name__ == '__main__':
    main()
