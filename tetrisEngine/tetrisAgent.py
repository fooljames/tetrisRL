from pygame.constants import *
import random

class TetrisAgent:
    possible_actions = [K_LEFT, K_RIGHT, K_UP, K_DOWN, 0]

    # main method to be put in RLinterface
    def tetrisAgent(self, state, reward=None):
        if state != 'terminal':
            return self.randomizeAction()
        else:
            return None

    # randomize an action to be played
    def randomizeAction(self):
        return random.choice(self.possible_actions)
