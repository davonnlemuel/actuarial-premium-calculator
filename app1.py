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

from products.endowment import (JointLifeEndowment, LastSurvivorEndowment)
from products.pure_endowment import (JointLifePureEndowment, LastSurvivorPureEndowment)

from products.anuitas import (
    JointLifeAnnuityDue,
    JointLifeWholeLifeAnnuityDue,
    LastSurvivorAnnuityDue,
    LastSurvivorWholeLifeAnnuityDue
)


def calculate(age1, age2, interest_rate,
              life_type,
              product_type,
              benefit_term=None,
              premium_term=None):

    male = MortalityTable("data/tmi_male.csv")
    female = MortalityTable("data/tmi_female.csv")

    interest = Interest(interest_rate)

    # joint life model selalu dipakai sebagai base
    joint = JointLife(male, female, age1, age2)


    # =========================
    # BENEFIT EPV
    # =========================

    if product_type == "term":

        if benefit_term is None:
            raise ValueError("Term insurance butuh benefit_term")

        if life_type == "joint":

            product = JointLifeTermInsurance(
                joint, interest, benefit_term
            )
            benefit_epv = product.epv_first_death()

        elif life_type == "last":

            product = LastSurvivorTermInsurance(
                male, female,
                age1, age2,
                interest,
                benefit_term,
                joint
            )
            benefit_epv = product.epv_last_death()

        else:
            raise ValueError("Life type tidak valid")


    elif product_type == "whole":

        if life_type == "joint":

            product = JointLifeWholeLifeInsurance(
                joint, interest
            )
            benefit_epv = product.epv_first_death()

        elif life_type == "last":

            product = LastSurvivorWholeLifeInsurance(
                male, female,
                age1, age2,
                interest,
                joint
            )
            benefit_epv = product.epv_last_death()

        else:
            raise ValueError("Life type tidak valid")


    elif product_type == "endowment":

        if benefit_term is None:
            raise ValueError("Endowment butuh benefit_term")

        if life_type == "joint":

            product = JointLifeEndowment(
                joint, interest, benefit_term
            )
            benefit_epv = product.epv_benefit()

        elif life_type == "last":

            product = LastSurvivorEndowment(
                male, female,
                age1, age2,
                interest,
                benefit_term,
                joint
            )
            benefit_epv = product.epv_benefit()

        else:
            raise ValueError("Life type tidak valid")


    elif product_type == "pure":

        if benefit_term is None:
            raise ValueError("Pure endowment butuh benefit_term")

        if life_type == "joint":

            product = JointLifePureEndowment(
                joint, interest, benefit_term
            )
            benefit_epv = product.epv_benefit()

        elif life_type == "last":

            product = LastSurvivorPureEndowment(
                male, female,
                age1, age2,
                interest,
                benefit_term,
                joint
            )
            benefit_epv = product.epv_benefit()

        else:
            raise ValueError("Life type tidak valid")


    else:
        raise ValueError("Product type tidak valid")


    # =========================
    # PREMIUM ANNUITY EPV
    # =========================

    if premium_term is None:
        raise ValueError("Premium term harus diisi")

    if life_type == "joint":

        if premium_term == "whole":

            annuity = JointLifeWholeLifeAnnuityDue(
                joint, interest
            )

        else:

            annuity = JointLifeAnnuityDue(
                joint, interest, premium_term
            )


    elif life_type == "last":

        if premium_term == "whole":

            annuity = LastSurvivorWholeLifeAnnuityDue(
                male, female,
                age1, age2,
                joint,
                interest
            )

        else:

            annuity = LastSurvivorAnnuityDue(
                male, female,
                age1, age2,
                joint,
                interest,
                premium_term
            )

    else:
        raise ValueError("Life type tidak valid")


    annuity_epv = annuity.epv()

    return benefit_epv, annuity_epv

