class JointLifeTermInsurance:
    def __init__(self, joint_life, interest, term):
        self.life = joint_life
        self.interest = interest
        self.term = term

    def epv_first_death(self):
        total = 0

        for t in range(self.term):
            survival = self.life.tpxy(t)
            death_prob = self.life.qxy(t)

            total += (self.interest.v ** (t+1)) * survival * death_prob

        return total
    
class LastSurvivorTermInsurance:

    def __init__(self, table1, table2, age1, age2, interest, term, joint_life):

        self.table1 = table1
        self.table2 = table2
        self.age1 = age1
        self.age2 = age2
        self.interest = interest
        self.term = term

        self.joint_life = joint_life


    def Ax(self):

        total = 0

        for t in range(self.term):

            survival = self.table1.tpx(self.age1, t)
            death = self.table1.qx(self.age1 + t)

            total += (self.interest.v ** (t+1)) * survival * death

        return total


    def Ay(self):

        total = 0

        for t in range(self.term):

            survival = self.table2.tpx(self.age2, t)
            death = self.table2.qx(self.age2 + t)

            total += (self.interest.v ** (t+1)) * survival * death

        return total


    def Axy(self):

        joint_term = JointLifeTermInsurance(
            self.joint_life,
            self.interest,
            self.term
        )

        return joint_term.epv_first_death()


    def epv_last_death(self):

        Ax = self.Ax()
        Ay = self.Ay()
        Axy = self.Axy()

        return Ax + Ay - Axy
