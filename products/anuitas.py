class JointLifeAnnuityDue:
    def __init__(self, joint_life, interest, term):
        self.life = joint_life
        self.interest = interest
        self.term = term

    def epv(self):
        epv = 0

        for t in range(self.term):
            survival = self.life.tpxy(t)
            epv += (self.interest.v ** t) * survival

        return epv  
    
class JointLifeWholeLifeAnnuityDue:
    def __init__(self, joint_life, interest):
        self.life = joint_life
        self.interest = interest

    def epv(self):
        epv = 0
        max_term = self.life.max_term()

        for t in range(max_term):
            survival = self.life.tpxy(t)
            epv += (self.interest.v ** t) * survival

        return epv
    
class LastSurvivorAnnuityDue:

    def __init__(self, table1, table2, age1, age2,
                 joint_life, interest, term):

        self.table1 = table1
        self.table2 = table2
        self.age1 = age1
        self.age2 = age2
        self.joint = joint_life
        self.interest = interest
        self.term = term


    def single_annuity(self, table, age):

        epv = 0

        for t in range(self.term):
            survival = table.tpx(age, t)
            epv += (self.interest.v ** t) * survival

        return epv


    def epv(self):

        ax = self.single_annuity(self.table1, self.age1)
        ay = self.single_annuity(self.table2, self.age2)

        axy = 0
        for t in range(self.term):
            survival = self.joint.tpxy(t)
            axy += (self.interest.v ** t) * survival

        return ax + ay - axy

class LastSurvivorWholeLifeAnnuityDue:

    def __init__(self, table1, table2, age1, age2,
                 joint_life, interest):

        self.table1 = table1
        self.table2 = table2
        self.age1 = age1
        self.age2 = age2
        self.joint = joint_life
        self.interest = interest


    def single_annuity(self, table, age):

        epv = 0
        max_term = self.joint.max_term()

        for t in range(max_term):
            survival = table.tpx(age, t)
            epv += (self.interest.v ** t) * survival

        return epv


    def epv(self):

        ax = self.single_annuity(self.table1, self.age1)
        ay = self.single_annuity(self.table2, self.age2)

        axy = 0
        max_term = self.joint.max_term()

        for t in range(max_term):
            survival = self.joint.tpxy(t)
            axy += (self.interest.v ** t) * survival

        return ax + ay - axy
