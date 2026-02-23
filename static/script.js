async function calculate() {

    // Detect halaman
    const isMultiple = document.getElementById("age1") !== null;

    let url = "";
    let data = {};

    if (isMultiple) {
        // ===== MULTIPLE LIFE =====
        url = "/calculate_multiple";

        data = {
            age1: document.getElementById("age1").value,
            age2: document.getElementById("age2").value,
            interest: document.getElementById("interest").value,
            life_type: document.getElementById("life_type").value,
            product_type: document.getElementById("product_type").value,
            benefit_term: document.getElementById("benefit_term").value || null,
            premium_term: document.getElementById("premium_term").value,
            sum_assured: document.getElementById("sum_assured").value
        };

    } else {
        // ===== SINGLE LIFE =====
        url = "/calculate_single";

        data = {
            age: document.getElementById("age").value,
            gender: document.getElementById("gender").value,
            interest: document.getElementById("interest").value,
            product_type: document.getElementById("product_type").value,
            benefit_term: document.getElementById("benefit_term").value || null,
            premium_term: document.getElementById("premium_term").value,
            sum_assured: document.getElementById("sum_assured").value
        };
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const err = await response.json();
            document.getElementById("result").innerHTML =
                "Error: " + (err.error || "Server error");
            return;
        }

        const result = await response.json();

        const formattedPremium = result.net_premium
            .toFixed(2)
            .replace(/\B(?=(\d{3})+(?!\d))/g, ",");

        document.getElementById("result").innerHTML =
            "<b>Net Premium:</b> " + formattedPremium + "<br>" +
            "<b>Benefit EPV:</b> " + result.benefit_epv.toFixed(6) + "<br>" +
            "<b>Annuity EPV:</b> " + result.annuity_epv.toFixed(6);

    } catch (error) {
        document.getElementById("result").innerHTML =
            "Unexpected error";
    }
}


function setupBenefitToggle(productId, benefitId) {
    const productSelect = document.getElementById(productId);
    const benefitInput = document.getElementById(benefitId);

    if (!productSelect || !benefitInput) return;

    function toggle() {
        if (productSelect.value === "whole") {
            benefitInput.disabled = true;
            benefitInput.value = "";
        } else {
            benefitInput.disabled = false;
        }
    }

    productSelect.addEventListener("change", toggle);
    toggle();
}

document.addEventListener("DOMContentLoaded", function () {
    setupBenefitToggle("product_type", "benefit_term");
});