const API_URL = "";

const form = document.getElementById("predictForm");
const result = document.getElementById("result");
const predictBtn = document.getElementById("predictBtn");

// Load dropdown options
async function loadOptions() {
    try {
        const response = await fetch(`${API_URL}/options`);

        if (!response.ok) {
            throw new Error("Unable to load options.");
        }

        const data = await response.json();

        fillSelect("cut", data.cut);
        fillSelect("color", data.color);
        fillSelect("clarity", data.clarity);

    } catch (error) {

        result.classList.add("show", "error");
        result.innerHTML = "❌ Failed to load dropdown options.";

        console.error(error);
    }
}

// Fill Select Menu
function fillSelect(id, options) {

    const select = document.getElementById(id);

    select.innerHTML = "";

    options.forEach(option => {

        const opt = document.createElement("option");

        opt.value = option;

        opt.textContent = option;

        select.appendChild(opt);

    });

}

// Predict Price
form.addEventListener("submit", async (e) => {

    e.preventDefault();

    predictBtn.classList.add("loading");
    predictBtn.disabled = true;

    predictBtn.innerHTML = "Predicting...";

    result.classList.remove("show", "error");
    result.innerHTML = "";

    const payload = {

        carat: parseFloat(document.getElementById("carat").value),

        cut: document.getElementById("cut").value,

        color: document.getElementById("color").value,

        clarity: document.getElementById("clarity").value,

        depth: parseFloat(document.getElementById("depth").value),

        table: parseFloat(document.getElementById("table").value),

        x: parseFloat(document.getElementById("x").value),

        y: parseFloat(document.getElementById("y").value),

        z: parseFloat(document.getElementById("z").value)

    };

    try {

        const response = await fetch(`${API_URL}/predict`, {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(payload)

        });

        const data = await response.json();

        result.classList.add("show");

        if (data.predicted_price) {

            const usdPrice = Number(data.predicted_price);

// Approximate conversion rate
const inrPrice = usdPrice * 86;

result.innerHTML = `
    <div style="font-size:18px;">💎 Estimated Diamond Price</div>
    <div style="font-size:36px;margin-top:10px;font-weight:700;color:#4ade80;">
        ₹ ${inrPrice.toLocaleString('en-IN')}
    </div>
    <div style="font-size:13px;color:#94a3b8;margin-top:8px;">
        (Approximate conversion from USD)
    </div>
`;

        } else {

            result.classList.add("error");

            result.innerHTML = `❌ ${data.error}`;

        }

    } catch (error) {

        result.classList.add("show", "error");

        result.innerHTML = "❌ Unable to connect to Flask API.";

        console.error(error);

    }

    predictBtn.classList.remove("loading");
    predictBtn.disabled = false;

    predictBtn.innerHTML = `
        <i class="fa-solid fa-wand-magic-sparkles"></i>
        Predict Price
    `;

});

// Start
loadOptions();