class JointLifeEndowment:
    def __init__(self, joint_life, interest, term):
        self.life = joint_life
        self.interest = interest
        self.term = term

    def epv_benefit(self):
        total = 0

        # ===== TERM INSURANCE PART =====
        for t in range(self.term):
            survival = self.life.tpxy(t)
            death_prob = self.life.qxy(t)

            total += (self.interest.v ** (t + 1)) * survival * death_prob

        # ===== PURE ENDOWMENT PART =====
        survival_to_n = self.life.tpxy(self.term)
        total += (self.interest.v ** self.term) * survival_to_n

        return total
    
class LastSurvivorEndowment:

    def __init__(self,
                 table1, table2,
                 age1, age2,
                 interest,
                 term,
                 joint_life):

        self.table1 = table1
        self.table2 = table2
        self.age1 = age1
        self.age2 = age2
        self.interest = interest
        self.term = term
        self.joint_life = joint_life


    # ===== TERM PART =====

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

        total = 0

        for t in range(self.term):

            survival = self.joint_life.tpxy(t)
            death = self.joint_life.qxy(t)

            total += (self.interest.v ** (t+1)) * survival * death

        return total


    # ===== PURE ENDOWMENT PART =====

    def Ex(self):

        return (self.interest.v ** self.term) * \
               self.table1.tpx(self.age1, self.term)


    def Ey(self):

        return (self.interest.v ** self.term) * \
               self.table2.tpx(self.age2, self.term)


    def Exy(self):

        return (self.interest.v ** self.term) * \
               self.joint_life.tpxy(self.term)


    # ===== FINAL =====

    def epv_benefit(self):

        term_part = self.Ax() + self.Ay() - self.Axy()

        pure_part = self.Ex() + self.Ey() - self.Exy()

        return term_part + pure_part
