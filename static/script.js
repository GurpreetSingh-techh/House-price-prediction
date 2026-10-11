const form = document.getElementById("predictionForm");

const button = document.getElementById("predictButton");

const buttonText = document.getElementById("buttonText");

const priceResult = document.getElementById("priceResult");

const resultMessage = document.getElementById("resultMessage");


form.addEventListener("submit", async function(event) {

    // Stop normal page refresh
    event.preventDefault();


    // Loading state
    button.classList.add("loading");

    buttonText.textContent = "Analyzing Property...";


    try {

        // Get form data
        const formData = new FormData(form);


        // Send data to Flask
        const response = await fetch("/predict", {

            method: "POST",

            body: formData

        });


        const data = await response.json();


        // Check result
        if (data.success) {

            const formattedPrice =
                new Intl.NumberFormat("en-US", {
                    style: "currency",
                    currency: "USD",
                    maximumFractionDigits: 0
                }).format(data.price);


            priceResult.textContent = formattedPrice;


            resultMessage.textContent =
                "Your property has been analyzed successfully using the trained machine learning model.";

        }

        else {

            priceResult.textContent = "Error";

            resultMessage.textContent =
                data.error;

        }


    }

    catch (error) {

        priceResult.textContent = "Error";

        resultMessage.textContent =
            "Something went wrong. Please check your Flask application.";

        console.error(error);

    }


    // Restore button
    button.classList.remove("loading");

    buttonText.textContent = "Predict House Price";

});
