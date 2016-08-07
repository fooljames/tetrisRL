class State(object):
    def __init__(self, col_height, max_height, height_diff, holes):
        self.col_height = col_height
        self.max_height = max_height
        self.height_diff = height_diff
        self.holes = holes
        self.transition = {
            'row': 0,
            'column': 0,
            'cell': 0
        }

    @classmethod
    def withTransition(cls, col_height, max_height, height_diff, holes, transition):
        temp = cls(col_height, max_height, height_diff, holes)
        temp.transition = transition
        return temp

    def updateTransition(self, previous):
        transition = {
            'row': 0,
            'column': 0,
            'cell': 0
        }
        return State.withTransition(self.col_height,
                                    self.max_height,
                                    self.height_diff,
                                    self.holes,
                                    transition)
