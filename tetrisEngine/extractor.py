import numpy as np


def extractFeature(state, nextPiece):
    shape = state.shape
    features = {'col_height': np.zeros(shape[1], dtype=np.int16),
                'max_height': 0,
                'height_diff': np.zeros(shape[1] - 1, dtype=np.int16),
                'holes': 0,
                'next_piece': nextPiece
                }
    for index, row in enumerate(state.T):
        ones = np.where(row[0] == 1)[1]
        if len(ones) > 0 :
            features['col_height'][index] = shape[0] - ones[0]
            features['holes'] += shape[0] - ones[0] - len(ones)
        if 0 < index < shape[1]:
            features['height_diff'][index-1] = features['col_height'][index] - features['col_height'][index-1]

    features['max_height'] = np.amax(features['col_height'])
    return features


def main():
    x = np.matrix([(0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0,1, 1), (0, 1, 0, 0, 0), (0, 1, 0, 0, 0),
                   (1, 1, 1, 1, 0), (1, 1, 1, 1, 0)])
    print x
    print "features: " + str(extractFeature(x, 2))


main()
