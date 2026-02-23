class JointLife:
    def __init__(self, table1, table2, age1, age2):
        self.table1 = table1
        self.table2 = table2
        self.age1 = age1
        self.age2 = age2

    def max_term(self):
        omega = 111
        return min(omega - self.age1,
               omega - self.age2)

    def tpxy(self, t):
        p1 = self.table1.tpx(self.age1, t)
        p2 = self.table2.tpx(self.age2, t)
        return p1 * p2
    
    def qxy(self, t):
        q1 = self.table1.qx(self.age1 + t)
        q2 = self.table2.qx(self.age2 + t)
        return 1 - (1 - q1)*(1 - q2)
    