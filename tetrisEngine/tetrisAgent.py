from pygame.constants import *
from abc import ABCMeta, abstractmethod
from utils import util
import featureExtractor
import random


class TetrisAgent(object):
    __metaclass__ = ABCMeta

    def __init__(self, env):
        self.lastState = None
        self.lastAction = None
        self.env = env

    # method for choosing an action
    @abstractmethod
    def agentChoose(self, state):
        pass

    # method for learning
    @abstractmethod
    def agentLearn(self, reward, state, next_action):
        pass

    # initialize new val when start a new episode
    @abstractmethod
    def agentStartEpisode(self, state):
        pass

    # main method to be put in RLinterface
    def agentFn(self, state, reward=None):

        if reward == None:
            self.agentStartEpisode(state)
        if state != 'terminal':
            next_action = self.agentChoose()

            self.agentLearn(reward, state, next_action)

            self.lastState, self.lastAction = state, next_action

            return next_action
        else:
            return None


class RandomAgent(TetrisAgent):
    def __init__(self, env):
        super(RandomAgent, self).__init__(env)

    def agentChoose(self):
        # randomize an action to be played
        return random.choice(self.env.get_legal_actions())

    def agentLearn(self, reward, state, next_action):
        super(RandomAgent, self).agentLearn(reward, state, next_action)

    def agentStartEpisode(self, state):
        super(RandomAgent, self).agentStartEpisode(state)


class ValueIterationAgent(TetrisAgent):
    def __init__(self, config):
        """
        :param
        config:
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        """
        super(ValueIterationAgent, self).__init__()
        self.epsilon = config['epsilon']
        self.gamma = config['gamma']
        self.alpha = config['alpha']

    def getLegalActions(self, state):
        return []

    @abstractmethod
    def getQValue(self, state, action):
        pass

    def getPolicy(self, state, legalActions):
        possibleStateQValues = util.Counter()

        for action in legalActions:
            possibleStateQValues[action] = self.getQValue(state, action)

        return possibleStateQValues.argMax()

    def agentChoose(self, state):

        legalActions = self.getLegalActions(state)
        if (random.random() <= self.epsilon):
            return random.choice(legalActions)
        else:
            return self.getPolicy(state, legalActions)


class SarsaApproxAgent(ValueIterationAgent):
    def __init__(self, config):
        super(SarsaApproxAgent, self).__init__(config)
        self.featureExtractor = getattr(featureExtractor, config['featureExtractor'])
        self.weights = util.Counter()

    def getQValue(self, state, action):
        qValue = 0.0
        next_state = getNextState(state, action)
        features = self.featureExtractor.extract(state, next_state)
        for key in features.keys():
            qValue += (self.weights[key] * features[key])
        return qValue

    def agentLearn(self, reward, state, next_action):
        features = self.featureExtractor.extract(self.lastState, state)
        err = reward + self.gamma * self.getQValue(state, next_action) - self.getQValue(self.lastState, self.lastAction)

        for key in features:
            self.weights[key] += self.alpha * err * features[key]


class QLearningApproxAgent(SarsaApproxAgent):
    def __init__(self, config):
        super(SarsaApproxAgent, self).__init__(config)

    def getValue(self, state):
        possibleStateQValues = util.Counter()
        for action in self.getLegalActions(state):
            possibleStateQValues[action] = self.getQValue(state, action)

        return possibleStateQValues[possibleStateQValues.argMax()]

    def agentLearn(self, reward, state, next_action):
        features = self.featureExtractor.extract(self.lastState, state)
        err = reward + self.gamma * self.getValue(state) - self.getQValue(self.lastState, self.lastAction)

        for key in features:
            self.weights[key] += self.alpha * err * features[key]
