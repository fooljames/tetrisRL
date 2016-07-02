from pygame.constants import *
import random

class TetrisAgent(object):
    possible_actions = [K_LEFT, K_RIGHT, K_UP, K_DOWN, 0]

    def __init__(self):
        self.fe = FeatureExtractor()

    # main method to be put in RLinterface
    def tetrisAgent(self, state, reward=None):
        features = self.fe.extract(state)

        if state != 'terminal':
            return self.randomizeAction()
        else:
            return None

    # randomize an action to be played
    def randomizeAction(self):
        return random.choice(self.possible_actions)


class FeatureExtractor(object):

    def __init__(self):
        pass

    def extract(self, state):
        pass
