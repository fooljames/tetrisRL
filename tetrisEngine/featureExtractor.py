import numpy as np
from state import State
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

    def extract(self, previous, current):
        shape = current.shape
        col_height = np.zeros(shape[1], dtype=np.int16)
        height_diff = np.zeros(shape[1] - 1, dtype=np.int16)
        holes = 0

        for index, row in enumerate(current.T):
            ones = np.where(row[0] == 1)[1]
            if len(ones) > 0:
                col_height[index] = shape[0] - ones[0]
                holes += shape[0] - ones[0] - len(ones)
            if 0 < index < shape[1]:
                height_diff[index - 1] = col_height[index] - col_height[index - 1]

        max_height = np.amax(col_height)

        state = State(col_height, max_height, height_diff, holes)

        state.updateTransition(previous)

        return state


def main():
    fe = SimpleFeatureExtractor()
    x = np.matrix([(0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 1, 1), (0, 1, 0, 0, 0), (0, 1, 0, 0, 0),
                   (1, 1, 1, 1, 0), (1, 1, 1, 1, 0)])
    print x
    print "features: " + str(fe.extract(x, x))

if __name__ == '__main__':
    main()
