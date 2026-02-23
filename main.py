from app import calculate
from pricing import NetPremiumCalculator


def main():

    age1 = 25
    age2 = 20
    interest_rate = 0.0475
    sum_assured = 1000000000

    # pilih life type
    life_type = "joint"   # "joint" atau "last"

    # pilih product
    product_type = "term"    #term, whole, pure, endowment

    benefit_term = 20
    premium_term = 10

    # =========================
    # ENGINE CALCULATION
    # =========================

    benefit_epv, annuity_epv = calculate(
        age1=age1,  
        age2=age2,
        interest_rate=interest_rate,
        life_type=life_type,
        product_type=product_type,
        benefit_term=benefit_term,
        premium_term=premium_term
    )

    # =========================
    # PRICING LAYER
    # =========================

    pricing = NetPremiumCalculator(
        benefit_epv,
        annuity_epv,
        sum_assured
    )

    net_premium = pricing.net_premium()
    benefit_value = pricing.benefit_value()

    # =========================
    # OUTPUT
    # =========================

    print("===================================")
    print(f"Life Type        : {life_type}")
    print(f"Product Type     : {product_type}")
    print(f"Benefit Term     : {benefit_term}")
    print(f"Premium Term     : {premium_term}")
    print(f"Sum Assured      : {sum_assured}")
    print("-----------------------------------")
    print("Unit EPV Benefit :", round(benefit_epv, 12))
    print("Unit EPV Annuity :", round(annuity_epv, 12))
    print("Benefit Value    :", round(benefit_value, 2))
    print("Net Premium      :", round(net_premium, 2))
    print("===================================")


if __name__ == "__main__":
    main()
