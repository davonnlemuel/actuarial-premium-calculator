class JointLifeWholeLifeInsurance:
    def __init__(self, joint_life, interest):
        self.life = joint_life
        self.interest = interest

    def epv_first_death(self):
        total = 0
        t = 0
        max_age = 111  # safety cap biar gak infinite loop

        while t < max_age:
            survival = self.life.tpxy(t)

            # kalau udah practically nol, berhenti
            if survival < 1e-12:
                break

            death_prob = self.life.qxy(t)

            total += (self.interest.v ** (t + 1)) * survival * death_prob

            t += 1

        return total
    
class LastSurvivorWholeLifeInsurance:

    def __init__(self, table1, table2, age1, age2, interest, joint_whole_life):

        self.table1 = table1
        self.table2 = table2

        self.age1 = age1
        self.age2 = age2

        self.interest = interest

        # reuse hasil joint life
        self.joint_whole_life = joint_whole_life


    def Ax(self):

        total = 0
        t = 0
        max_age = 111

        while t < max_age:

            survival = self.table1.tpx(self.age1, t)

            if survival < 1e-12:
                break

            death_prob = self.table1.qx(self.age1 + t)

            total += (self.interest.v ** (t + 1)) * survival * death_prob

            t += 1

        return total


    def Ay(self):

        total = 0
        t = 0
        max_age = 111

        while t < max_age:

            survival = self.table2.tpx(self.age2, t)

            if survival < 1e-12:
                break

            death_prob = self.table2.qx(self.age2 + t)

            total += (self.interest.v ** (t + 1)) * survival * death_prob

            t += 1

        return total


    def epv_last_death(self):

        Ax = self.Ax()
        Ay = self.Ay()
        Axy = self.joint_whole_life.epv_first_death()

        return Ax + Ay - Axy
