import pandas as pd

class MortalityTable:
    def __init__(self, filepath):
        self.table = pd.read_csv(filepath)

    def qx(self, age):
        return self.table.loc[self.table["x"] == age, "qx"].values[0]

    def px(self, age):
        return self.table.loc[self.table["x"] == age, "px"].values[0]

    def tpx(self, age, t):
        prob = 1.0
        for k in range(t):
            prob *= self.px(age + k)
        return prob