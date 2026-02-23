class NetPremiumCalculator:
    def __init__(self, benefit_epv, annuity_epv, sum_assured=1):
        self.benefit_epv = benefit_epv
        self.annuity_epv = annuity_epv
        self.sum_assured = sum_assured

    def net_premium(self):
        return (self.sum_assured * self.benefit_epv) / self.annuity_epv

    def benefit_value(self):
        return self.sum_assured * self.benefit_epv