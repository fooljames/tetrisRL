from tetrisEnv import *
from tetrisAgent import *
from RLtoolkit.RLinterface import RLinterface


def main():
    env = TetrisEnv()
    agent = TetrisAgent()
    rli = RLinterface(agent.tetrisAgent, env.tetris_env)
    # run two episodes of tetris and print state, action, reward for every step
    episode = rli.episodes(1)
    print episode[3]


if __name__ == '__main__':
    main()
