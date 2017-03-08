import numpy as np
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
        current = np.matrix(present[0])
        shape = current[0].shape
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

        features = {'col_height': np.sum(col_height),
                    'max_height': max_height,
                    'height_diff': np.sum(height_diff),
                    'holes': holes}


        # state = State(col_height, max_height, height_diff, holes)

        # state.updateTransition(previous)

        return features


def main():
    fe = SimpleFeatureExtractor()
    x = np.matrix([(0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 1, 1), (0, 1, 0, 0, 0), (0, 1, 0, 0, 0),
                   (1, 1, 1, 1, 0), (1, 1, 1, 1, 0)])
    print x
    print "features: " + str(fe.extract(x, x))

    features = fe.extract(x, x)
    for key in features:
        print 0.1* features[key] + 3

if __name__ == '__main__':
    main()
