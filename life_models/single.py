import math
import pandas as pd

# Gompertz-Makeham Model untuk TMI

class MortalityTable:
    def __init__(self, min_age=0, max_age=120):
        # Standard Gompertz-Makeham parameters (reasonable actuarial demo values)
        self.A = 0.00022
        self.B = 2.7e-6
        self.c = 1.124
        
        self.min_age = min_age
        self.max_age = max_age
        
        self.table = self._generate_table()
    
    def force_of_mortality(self, age):
        return self.A + self.B * (self.c ** age)
    
    def qx(self, age):
        if age >= self.max_age:
            return 1.0
        mu = self.force_of_mortality(age)
        return 1 - math.exp(-mu)
    
    def px(self, age):
        return 1 - self.qx(age)
    
    def _generate_table(self):
        data = []
        for age in range(self.min_age, self.max_age + 1):
            data.append({
                "age": age,
                "qx": self.qx(age),
                "px": self.px(age)
            })
        return pd.DataFrame(data)


# Fungsi Survival

def npx(table, x, k):
    prob = 1.0
    for t in range(k):
        prob *= table.px(x + t)
    return prob

# EPV untuk jenis" asuransi pilihan nasabah

# Term Insurance
def term_insurance_epv(table, x, n, i):
    v = 1 / (1 + i)
    epv = 0.0
    for k in range(n):
        survival = npx(table, x, k)
        death = table.qx(x + k)
        epv += (v ** (k + 1)) * survival * death
    return epv


# Whole Life Insurance
def whole_life_epv(table, x, i):
    v = 1 / (1 + i)
    epv = 0.0
    max_term = table.max_age - x
    
    for k in range(max_term):
        survival = npx(table, x, k)
        death = table.qx(x + k)
        epv += (v ** (k + 1)) * survival * death
    
    return epv


# Pure Endowment
def pure_endowment_epv(table, x, n, i):
    v = 1 / (1 + i)
    survival = npx(table, x, n)
    return (v ** n) * survival


# Endowment Insurance (Term + Pure Endowment)
def endowment_epv(table, x, n, i):
    term_part = term_insurance_epv(table, x, n, i)
    pure_part = pure_endowment_epv(table, x, n, i)
    return term_part + pure_part

# EPV Annuity Due
def annuity_due_epv(table, x, m, i):
    v = 1 / (1 + i)
    epv = 0.0
    
    for k in range(m):
        survival = npx(table, x, k)
        epv += (v ** k) * survival
    
    return epv


# Net Premium
def calculate_premium(product_type, age, benefit_term, premium_term, sum_assured, interest):
    table = MortalityTable()
    
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
    
    a = annuity_due_epv(table, age, premium_term, interest)
    
    benefit_value = sum_assured * A
    premium = benefit_value / a
    
    return A, a, benefit_value, premium


# MASUKIN PARAMETER" KITA DISINI

product_type = "term"   # "term", "whole", "pure_endowment", "endowment"
age = 30
benefit_term = 20
premium_term = 20
sum_assured = 100_000_000
interest = 0.05


A, a, benefit_value, premium = calculate_premium(
    product_type,
    age,
    benefit_term,
    premium_term,
    sum_assured,
    interest
)

# Output

print("Product Type     :", product_type.upper())
print("Age              :", age)
print("Benefit Term     :", benefit_term)
print("Premium Term     :", premium_term)
print("Benefit          :", sum_assured)
print("--------------------------------------------")
print("Unit EPV Benefit :", round(A, 10))
print("Unit EPV Annuity :", round(a, 10))
print("Benefit Value    :", round(benefit_value, 2))
print("Net Premium      :", round(premium, 2))