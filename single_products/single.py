import pandas as pd


# =========================
# MORTALITY TABLE
# =========================

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


# =========================
# EPV FUNCTIONS
# =========================

def term_insurance_epv(table, x, n, i):
    v = 1 / (1 + i)
    epv = 0.0

    for k in range(n):
        survival = table.tpx(x, k)
        death = table.qx(x + k)
        epv += (v ** (k + 1)) * survival * death

    return epv


def whole_life_epv(table, x, i):
    v = 1 / (1 + i)
    epv = 0.0
    max_term = 111 - x

    for k in range(max_term):
        survival = table.tpx(x, k)
        death = table.qx(x + k)
        epv += (v ** (k + 1)) * survival * death

    return epv


def pure_endowment_epv(table, x, n, i):
    v = 1 / (1 + i)
    survival = table.tpx(x, n)
    return (v ** n) * survival


def endowment_epv(table, x, n, i):
    return (
        term_insurance_epv(table, x, n, i)
        + pure_endowment_epv(table, x, n, i)
    )


def annuity_due_epv(table, x, m, i):
    v = 1 / (1 + i)
    epv = 0.0

    for k in range(m):
        survival = table.tpx(x, k)
        epv += (v ** k) * survival

    return epv

def whole_life_annuity_due_epv(table, x, i):
    v = 1 / (1 + i)
    epv = 0.0
    k = 0

    while True:
        survival = table.tpx(x, k)

        # kalau survival udah 0, stop
        if survival <= 0:
            break

        epv += (v ** k) * survival
        k += 1

        # safety stop (misal max age 111)
        if x + k > 111:
            break

    return epv


# =========================
# MAIN CALCULATION FUNCTION
# =========================

def calculate_premium(product_type,
                      gender,
                      age,
                      benefit_term,
                      premium_term,
                      sum_assured,
                      interest):

    # Mortality table selection
    if gender.lower() == "male":
        filepath = "data/tmi_male.csv"
    elif gender.lower() == "female":
        filepath = "data/tmi_female.csv"
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    table = MortalityTable(filepath)

    # =========================
    # BENEFIT EPV (UNIT)
    # =========================

    if product_type == "term":
        A = term_insurance_epv(table, age, benefit_term, interest)

    elif product_type == "whole":
        A = whole_life_epv(table, age, interest)

    elif product_type == "pure_endowment":
        A = pure_endowment_epv(table, age, benefit_term, interest)

    elif product_type == "endowment":
        A = endowment_epv(table, age, benefit_term, interest)

    else:
        raise ValueError("Unknown product type")

    # =========================
    # ANNUITY EPV (UNIT)
    # =========================

    if premium_term == "whole":
        a = whole_life_annuity_due_epv(table, age, interest)
    else:
        a = annuity_due_epv(table, age, premium_term, interest)

    # =========================
    # NET PREMIUM
    # =========================

    benefit_value = sum_assured * A

    if a == 0:
        raise ValueError("Annuity EPV = 0, tidak bisa bagi nol")

    premium = benefit_value / a

    return A, a, benefit_value, premium