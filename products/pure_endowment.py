class JointLifePureEndowment:
    def __init__(self, joint_life, interest, term):
        self.life = joint_life
        self.interest = interest
        self.term = term

    def epv_benefit(self):
        survival_to_n = self.life.tpxy(self.term)
        return (self.interest.v ** self.term) * survival_to_n
    
class LastSurvivorPureEndowment:

    def __init__(self, table1, table2, age1, age2, interest, term, joint_life):

        self.table1 = table1
        self.table2 = table2
        self.age1 = age1
        self.age2 = age2
        self.interest = interest
        self.term = term
        self.joint_life = joint_life


    def Ex(self):

        return (self.interest.v ** self.term) * \
               self.table1.tpx(self.age1, self.term)


    def Ey(self):

        return (self.interest.v ** self.term) * \
               self.table2.tpx(self.age2, self.term)


    def Exy(self):

        return (self.interest.v ** self.term) * \
               self.joint_life.tpxy(self.term)


    def epv_benefit(self):

        return self.Ex() + self.Ey() - self.Exy()
