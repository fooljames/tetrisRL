import numpy as np
from utils import util
from State import State
from abc import ABCMeta, abstractmethod


class FeatureExtractor(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def extract(self, previous, current):
        pass


class SimpleFeatureExtractor(FeatureExtractor):
    def __init__(self):
        super(SimpleFeatureExtractor, self).__init__()

    def extract(self, previous, present):

        ## QUESTIONS
        # # 1. How are states represented? x, y axes. when printed and stuff
        # # 2. Falling piece, x, y
        # # 3. Features supposed to be extracted for previous or present? => should be present.

        ##todo check whether needed to be transposed
        current_board = np.transpose(np.matrix(present[0]))
        piece = present[1]['shape']

        features = util.Counter()

        shape = current_board[0].shape
        col_height = np.zeros(shape[1], dtype=np.int16)
        height_diff = np.zeros(shape[1] - 1, dtype=np.int16)
        holes = 0

        for index, row in enumerate(current_board.T):
            ones = np.where(row[0] == 1)[1]
            if len(ones) > 0:
                col_height[index] = shape[0] - ones[0]
                holes += shape[0] - ones[0] - len(ones)
            if 0 < index < shape[1]:
                height_diff[index - 1] = col_height[index] - col_height[index - 1]

        max_height = np.amax(col_height)

        for i,r in enumerate(col_height):
            features[piece + "_col_h_" + str(i)] = col_height[i]

        features[piece + "_max_h"] = max_height

        for i,r in enumerate(height_diff):
            features[piece + "_diff_h_" + str(i) + "_" + str(i+1)] = height_diff[i]

        features[piece + "_holes"] = holes
        # print features

        # state = State(col_height, max_height, height_diff, holes)

        # state.updateTransition(previous)

        return features


def main():
    fe = SimpleFeatureExtractor()
    x = ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
         {'y': -2, 'x': 3, 'shape': 'L', 'rotation': 2, 'color': 0})

    # print x
    # print "features: " + str(fe.extract(x, x))

    features = fe.extract(x, x)
    for key in features:
        print features[key]

if __name__ == '__main__':
    main()
