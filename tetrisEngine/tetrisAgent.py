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
            next_action = self.agentChoose(state)

            self.agentLearn(reward, state, next_action)

            self.lastState, self.lastAction = state, next_action

            print "##################complete##################"

            return next_action
        else:
            return None


class RandomAgent(TetrisAgent):
    def __init__(self, env):
        super(RandomAgent, self).__init__(env)

    def agentChoose(self, state):
        # randomize an action to be played
        return random.choice(self.env.get_legal_actions())

    def agentLearn(self, reward, state, next_action):
        super(RandomAgent, self).agentLearn(reward, state, next_action)

    def agentStartEpisode(self, state):
        super(RandomAgent, self).agentStartEpisode(state)


class ValueIterationAgent(TetrisAgent):
    def __init__(self, env, config):
        """
        :param
        config:
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        """
        super(ValueIterationAgent, self).__init__(env)
        self.epsilon = config['epsilon']
        self.gamma = config['gamma']
        self.alpha = config['alpha']
        self.featureExtractor = config['featureExtractor']
        self.weights = util.Counter()

    def getQValue(self, state, action):
        qValue = 0.0
        next_state = self.getNextState(state, action)
        # print "next state"
        # print next_state
        if next_state[0] != 'terminal':
            features = self.featureExtractor.extract(state, next_state)
            for key in features.keys():
                self.weights[key] += 1
                qValue += (self.weights[key] * features[key])
        else:
            #TODO what should be this value ?
            qValue = -100.0

        return qValue

    def getPolicy(self, state, legalActions):

        possibleStateQValues = util.Counter()

        print "getting policy"

        for action in legalActions:
            possibleStateQValues[legalActions.index(action)] = self.getQValue(state, action)

        print possibleStateQValues

        index = possibleStateQValues.argMax()
        next_action = legalActions[index]

        print "**************next action************"
        print next_action

        return next_action

    def agentChoose(self, state):

        legalActions = self.env.get_legal_actions()
        print "legal actions"
        print legalActions

        if (random.random() <= self.epsilon):
            print "return random"
            return random.choice(legalActions)
        else:
            return self.getPolicy(state, legalActions)

    def getNextState(self, state, action):
        return state
        print "---------------------"
        print "for action"
        print action

        next = self.env.getStateAfterActions(action, False)

        if next[0] == 'terminal':
            next_state = 'terminal'
            falling_piece = None
        else:
            next_state = self.env.fn(next[0].board)
            falling_piece = next[0].fallingPiece

        print "next state"
        print state
        return next_state, falling_piece
        # return state

    def agentStartEpisode(self, state):
        super(ValueIterationAgent, self).agentStartEpisode(state)


class SarsaApproxAgent(ValueIterationAgent):
    def __init__(self, env, config):
        super(SarsaApproxAgent, self).__init__(env, config)

    def agentLearn(self, reward, state, next_action):
        features = self.featureExtractor.extract(self.lastState, state)
        err = reward + self.gamma * self.getQValue(state, next_action) - self.getQValue(self.lastState, self.lastAction)

        for key in features:
            self.weights[key] += self.alpha * err * features[key]


class QLearningApproxAgent(ValueIterationAgent):
    def __init__(self, env, config):
        super(QLearningApproxAgent, self).__init__(env, config)

    def getValue(self, state):
        print "getting value for the current action"
        possibleStateQValues = util.Counter()

        legalActions = self.env.get_legal_actions()
        for action in legalActions:
            possibleStateQValues[legalActions.index(action)] = self.getQValue(state, action)

        selected = possibleStateQValues[possibleStateQValues.argMax()]

        print "possibleStateQValues"
        print possibleStateQValues
        print "selected"
        print selected

        return selected

    def agentLearn(self, reward, state, next_action):
        features = self.featureExtractor.extract(self.lastState, state)

        print "getting the features"
        print features

        if reward == None or reward == 0:
            reward = 0
        else:
            print "reward"
            print reward
            print "last state is"
            print self.lastState
            print "last action"
            print self.lastAction
            if self.lastState == None:
                err = 0.0
            else:
                err = reward + self.gamma * self.getValue(state) - self.getQValue(self.lastState, self.lastAction)
                print "err"
                print err
            for key in features:
                self.weights[key] += self.alpha * err * features[key]







