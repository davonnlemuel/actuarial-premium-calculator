#ini mah tapi gadipake buat epc, pake rumus matas aj

class LastSurvivor:
    def __init__(self, table1, table2, age1, age2):
        self.table1 = table1
        self.table2 = table2
        self.age1 = age1
        self.age2 = age2

    def tpxy(self, t):
        p1 = self.table1.tpx(self.age1, t)
        p2 = self.table2.tpx(self.age2, t)
        return 1 - (1 - p1) * (1 - p2)

    def qxy(self, t):
        p_t = self.tpxy(t)
        p_t1 = self.tpxy(t + 1)
        return p_t - p_t1