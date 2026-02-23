from life_models.mortality_table import MortalityTable

print("ini buat cek ke data tmi")
male = MortalityTable("data/tmi_male.csv")

print("qx(25):", male.qx(25))
print("px(25):", male.px(25))
print("5-year survival (male) from 25:", male.tpx(25, 5))


from life_models.mortality_table import MortalityTable
from life_models.joint_life import JointLife

print("ini buat cek joint life")
male = MortalityTable("data/tmi_male.csv")
female = MortalityTable("data/tmi_female.csv")

joint = JointLife(male, female, 25, 20)

print("5-year joint survival:", joint.tpxy(5))
print(joint.qxy(5))

# =========================
# Last Survivor test
# =========================

from life_models.last_survivor import LastSurvivor

print("\nini buat cek last survivor")

male = MortalityTable("data/tmi_male.csv")
female = MortalityTable("data/tmi_female.csv")

last = LastSurvivor(male, female, 25, 20)

print("5-year last survivor survival:", last.tpxy(5))
print("last survivor death probability in year 5:", last.qxy(5))