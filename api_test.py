# ini versi sebelum validasi age bukan diskret

from flask import Flask, request, jsonify, render_template
from app import calculate, calculate_single
from pricing import NetPremiumCalculator
import pandas as pd

app = Flask(__name__)

# ===== PAGE ROUTES =====

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/multiple")
def multiple():
    return render_template("multiple.html")

@app.route("/single")
def single():
    return render_template("single.html")

@app.route("/description")
def description():
    return render_template("description.html")

# ===== MORTALITY VISUALIZATION =====

@app.route("/qx")
def qx():

    male = pd.read_csv("data/tmi_male.csv")
    female = pd.read_csv("data/tmi_female.csv")

    ages = male["x"].tolist()
    qx_male = male["qx"].tolist()
    qx_female = female["qx"].tolist()

    table_male = male.to_html(classes="table", index=False)
    table_female = female.to_html(classes="table", index=False)

    return render_template(
        "visualisasi.html",
        ages=ages,
        qx_male=qx_male,
        qx_female=qx_female,
        table_male=table_male,
        table_female=table_female
    )


# ===============================
# ===== MULTIPLE CALCULATOR =====
# ===============================

@app.route("/calculate_multiple", methods=["POST"])
def calculate_multiple_api():
    try:
        data = request.json

        age1 = int(data["age1"])
        age2 = int(data["age2"])
        interest = float(data["interest"])
        life_type = data["life_type"]
        product_type = data["product_type"]

        benefit_term = data.get("benefit_term")
        premium_term = data.get("premium_term")

        if benefit_term is not None:
            benefit_term = int(benefit_term)

        if premium_term is None:
            raise ValueError("Premium term harus diisi")

        premium_term = premium_term.strip().lower()

        if premium_term != "whole":
            premium_term = int(premium_term)

        sum_assured = float(data["sum_assured"])

        benefit_epv, annuity_epv = calculate(
            age1,
            age2,
            interest,
            life_type,
            product_type,
            benefit_term,
            premium_term
        )

        pricing = NetPremiumCalculator(
            benefit_epv,
            annuity_epv,
            sum_assured
        )

        result = {
            "net_premium": pricing.net_premium(),
            "benefit_epv": benefit_epv,
            "annuity_epv": annuity_epv
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ===============================
# ===== SINGLE CALCULATOR ======
# ===============================

@app.route("/calculate_single", methods=["POST"])
def calculate_single_api():
    try:
        data = request.json

        age = int(data["age"])
        gender = data["gender"]
        interest = float(data["interest"])
        product_type = data["product_type"]

        benefit_term = data.get("benefit_term")
        premium_term = data.get("premium_term")

        # convert only if needed
        if benefit_term is not None and benefit_term != "":
            benefit_term = int(benefit_term)
        else:
            benefit_term = None

        if premium_term is None:
            raise ValueError("Premium term harus diisi")

        premium_term = premium_term.strip().lower()

        if premium_term != "whole":
            premium_term = int(premium_term)

        sum_assured = float(data["sum_assured"])

        benefit_epv, annuity_epv = calculate_single(
            age,
            gender,
            interest,
            product_type,
            benefit_term,
            premium_term,
            sum_assured
        )

        pricing = NetPremiumCalculator(
            benefit_epv,
            annuity_epv,
            sum_assured
        )

        result = {
            "net_premium": pricing.net_premium(),
            "benefit_epv": benefit_epv,
            "annuity_epv": annuity_epv
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)