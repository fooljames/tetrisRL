from pygame.constants import *
from abc import ABCMeta, abstractmethod
import random

class TetrisAgent(object):
    __metaclass__ = ABCMeta

    possible_actions = [K_LEFT, K_RIGHT, K_UP, K_DOWN, 0]

    def __init__(self):
        self.lastState = None
        self.lastAction = None

    # method for choosing an action
    @abstractmethod
    def agentChoose(self, state):
        pass

    # method for learning
    @abstractmethod
    def agentLearn(self, reward, state):
        pass

    # initialize new val when start a new episode
    @abstractmethod
    def agentStartEpisode(self, state):
        pass

    # main method to be put in RLinterface
    def agentFn(self, state, reward=None):

        if reward != None:
            self.agentLearn(reward, state)
        else:
            self.agentStartEpisode(state)
        if state != 'terminal':
            action = self.agentChoose(state)
            self.lastState, self.lastAction = state, action

            return action
        else:
            return None


class RandomAgent(TetrisAgent):
    def __init__(self):
        super(RandomAgent, self).__init__()

    def agentChoose(self, state):
        # randomize an action to be played
        return random.choice(self.possible_actions)

    def agentLearn(self, reward, state):
        super(RandomAgent, self).agentLearn(reward, state)

    def agentStartEpisode(self, state):
        super(RandomAgent, self).agentStartEpisode(state)
