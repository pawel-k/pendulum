class Dataset(object):
    def __init__(self):
        self._data = []
        self._target = []

    @property
    def data(self):
        return self._data

    @property
    def target(self):
        return self._target

    def add_case(self,situation, action):
        self.data.append(situation)
        self.target.append(action)
