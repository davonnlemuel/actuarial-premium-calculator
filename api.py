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

        # ===== AGE 1 =====
        age1_raw = data["age1"]
        if not float(age1_raw).is_integer():
            raise ValueError("Age male harus bilangan bulat")
        age1 = int(age1_raw)

        # ===== AGE 2 =====
        age2_raw = data["age2"]
        if not float(age2_raw).is_integer():
            raise ValueError("Age female harus bilangan bulat")
        age2 = int(age2_raw)

        interest = float(data["interest"])
        life_type = data["life_type"]
        product_type = data["product_type"]

        # ===== BENEFIT TERM =====
        benefit_term_raw = data.get("benefit_term")

        if benefit_term_raw not in [None, ""]:
            if not float(benefit_term_raw).is_integer():
                raise ValueError("Benefit term harus bilangan bulat")
            benefit_term = int(benefit_term_raw)
        else:
            benefit_term = None

        # ===== PREMIUM TERM =====
        premium_term_raw = data.get("premium_term")

        if premium_term_raw is None:
            raise ValueError("Premium term harus diisi")

        premium_term_raw = premium_term_raw.strip().lower()

        if premium_term_raw != "whole":
            if not float(premium_term_raw).is_integer():
                raise ValueError("Premium term harus bilangan bulat")
            premium_term = int(premium_term_raw)
        else:
            premium_term = "whole"

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

        return jsonify({
            "net_premium": pricing.net_premium(),
            "benefit_epv": benefit_epv,
            "annuity_epv": annuity_epv
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ===============================
# ===== SINGLE CALCULATOR ======
# ===============================

@app.route("/calculate_single", methods=["POST"])
def calculate_single_api():
    try:
        data = request.json

        # ===== AGE =====
        age_raw = data["age"]
        if not float(age_raw).is_integer():
            raise ValueError("Umur harus bilangan bulat")
        age = int(age_raw)

        gender = data["gender"]
        interest = float(data["interest"])
        product_type = data["product_type"]

        # ===== BENEFIT TERM =====
        benefit_term_raw = data.get("benefit_term")

        if benefit_term_raw not in [None, ""]:
            if not float(benefit_term_raw).is_integer():
                raise ValueError("Benefit term harus bilangan bulat")
            benefit_term = int(benefit_term_raw)
        else:
            benefit_term = None

        # ===== PREMIUM TERM =====
        premium_term_raw = data.get("premium_term")

        if premium_term_raw is None:
            raise ValueError("Premium term harus diisi")

        premium_term_raw = premium_term_raw.strip().lower()

        if premium_term_raw != "whole":
            if not float(premium_term_raw).is_integer():
                raise ValueError("Premium term harus bilangan bulat")
            premium_term = int(premium_term_raw)
        else:
            premium_term = "whole"

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

        return jsonify({
            "net_premium": pricing.net_premium(),
            "benefit_epv": benefit_epv,
            "annuity_epv": annuity_epv
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)