from life_models.mortality_table import MortalityTable
from life_models.joint_life import JointLife
from finance.interest import Interest

from products.term import (
    JointLifeTermInsurance,
    LastSurvivorTermInsurance
)

from products.whole_life import (
    JointLifeWholeLifeInsurance,
    LastSurvivorWholeLifeInsurance
)

from products.endowment import (
    JointLifeEndowment,
    LastSurvivorEndowment
)

from products.pure_endowment import (
    JointLifePureEndowment,
    LastSurvivorPureEndowment
)

from products.anuitas import (
    JointLifeAnnuityDue,
    JointLifeWholeLifeAnnuityDue,
    LastSurvivorAnnuityDue,
    LastSurvivorWholeLifeAnnuityDue
)

# ======================================
# MULTIPLE LIFE CALCULATION
# ======================================

def calculate(age1, age2, interest_rate, life_type, product_type,
              benefit_term=None, premium_term=None):

    male = MortalityTable("data/tmi_male.csv")
    female = MortalityTable("data/tmi_female.csv")
    interest = Interest(interest_rate)

    joint = JointLife(male, female, age1, age2)

    omega = 111

    if age1 >= omega or age2 >= omega:
        raise ValueError("Umur melebihi batas maksimum tabel mortalita")

    if benefit_term is not None and benefit_term <= 0:
        raise ValueError("Benefit term harus positif")

    if premium_term != "whole" and premium_term <= 0:
        raise ValueError("Premium term harus positif")

    if benefit_term is not None:
        if life_type == "joint" or life_type == "last":
            max_term = min(omega - age1, omega - age2)
        else:
            max_term = omega - age1

        if benefit_term > max_term:
            raise ValueError("Benefit term melewati umur maksimum")

    # =========================
    # BENEFIT EPV
    # =========================

    if product_type == "term":
        if benefit_term is None:
            raise ValueError("Term insurance butuh benefit_term")

        if life_type == "joint":
            product = JointLifeTermInsurance(joint, interest, benefit_term)
            benefit_epv = product.epv_first_death()
        elif life_type == "last":
            product = LastSurvivorTermInsurance(
                male, female, age1, age2, interest, benefit_term, joint
            )
            benefit_epv = product.epv_last_death()
        else:
            raise ValueError("Life type tidak valid")

    elif product_type == "whole":
        if life_type == "joint":
            product = JointLifeWholeLifeInsurance(joint, interest)
            benefit_epv = product.epv_first_death()
        elif life_type == "last":
            joint_whole_life = JointLifeWholeLifeInsurance(joint, interest)

            product = LastSurvivorWholeLifeInsurance(
                male,
                female,
                age1,
                age2,
                interest,
                joint_whole_life
            )

            benefit_epv = product.epv_last_death()
        else:
            raise ValueError("Life type tidak valid")

    elif product_type == "endowment":
        if benefit_term is None:
            raise ValueError("Endowment butuh benefit_term")

        if life_type == "joint":
            product = JointLifeEndowment(joint, interest, benefit_term)
        elif life_type == "last":
            product = LastSurvivorEndowment(
                male, female, age1, age2, interest, benefit_term, joint
            )
        else:
            raise ValueError("Life type tidak valid")

        benefit_epv = product.epv_benefit()

    elif product_type == "pure":
        if benefit_term is None:
            raise ValueError("Pure endowment butuh benefit_term")

        if life_type == "joint":
            product = JointLifePureEndowment(joint, interest, benefit_term)
        elif life_type == "last":
            product = LastSurvivorPureEndowment(
                male, female, age1, age2, interest, benefit_term, joint
            )
        else:
            raise ValueError("Life type tidak valid")

        benefit_epv = product.epv_benefit()

    else:
        raise ValueError("Product type tidak valid")

    # =========================
    # PREMIUM ANNUITY EPV
    # =========================

    if premium_term is None:
        raise ValueError("Premium term harus diisi")

    if premium_term != "whole":
        if life_type in ["joint", "last"]:
            max_prem_term = min(omega - age1, omega - age2)
        else:
            max_prem_term = omega - age1

        if premium_term > max_prem_term:
            raise ValueError("Premium term melewati umur maksimum")

    if life_type == "joint":
        if premium_term == "whole":
            annuity = JointLifeWholeLifeAnnuityDue(joint, interest)
        else:
            annuity = JointLifeAnnuityDue(joint, interest, premium_term)

    elif life_type == "last":
        if premium_term == "whole":
            annuity = LastSurvivorWholeLifeAnnuityDue(
                male, female, age1, age2, joint, interest
            )
        else:
            annuity = LastSurvivorAnnuityDue(
                male, female, age1, age2, joint, interest, premium_term
            )
    else:
        raise ValueError("Life type tidak valid")

    annuity_epv = annuity.epv()

    return benefit_epv, annuity_epv


# ======================================
# SINGLE LIFE CALCULATION (WRAPPER)
# ======================================

from single_products.single import calculate_premium


def calculate_single(age, gender, interest_rate, product_type,
                     benefit_term=None, premium_term=None,
                     sum_assured=None):

    omega = 111

    # =========================
    # BASIC VALIDATION
    # =========================

    if age >= omega:
        raise ValueError("Umur melebihi batas maksimum tabel mortalita")

    if premium_term is None:
        raise ValueError("Premium term harus diisi")

    if product_type in ["term", "pure_endowment", "endowment"] and benefit_term is None:
        raise ValueError("Benefit term harus diisi untuk produk ini")

    if benefit_term is not None and benefit_term <= 0:
        raise ValueError("Benefit term harus positif")

    if premium_term != "whole" and premium_term <= 0:
        raise ValueError("Premium term harus positif")

    # =========================
    # MAX TERM VALIDATION
    # =========================

    max_term = omega - age

    if benefit_term is not None and benefit_term > max_term:
        raise ValueError("Benefit term melewati umur maksimum")

    if premium_term != "whole" and premium_term > max_term:
        raise ValueError("Premium term melewati umur maksimum")

    # =========================
    # CALCULATION
    # =========================

    A, a, benefit_value, premium = calculate_premium(
        product_type=product_type,
        gender=gender,
        age=age,
        benefit_term=benefit_term,
        premium_term=premium_term,
        sum_assured=sum_assured,
        interest=interest_rate
    )

    return A, a