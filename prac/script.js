function calculateBMI() {
    // Get user inputs
    const weight = parseFloat(document.getElementById("weight").value);
    const height = parseFloat(document.getElementById("height").value);
    const bmiResultDiv = document.getElementById("bmiResult");

    // Calculate BMI
    const bmi = weight / (height * height);
    const bmiOutput = document.getElementById("bmiOutput");

    // Display BMI result
    bmiOutput.innerText = `Your BMI is: ${bmi.toFixed(2)}`;
    bmiResultDiv.style.display = "block";

    // Determine BMI category and highlight the appropriate row
    document
    .querySelectorAll("tbody tr")
    .forEach((row) => row.classList.remove("highlight"));

    if (bmi < 18.5) {
    document.getElementById("underweight").classList.add("highlight");
    } else if (bmi >= 18.5 && bmi <= 24.9) {
    document.getElementById("normal").classList.add("highlight");
    } else if (bmi >= 25 && bmi <= 29.9) {
    document.getElementById("overweight").classList.add("highlight");
    } else {
    document.getElementById("obese").classList.add("highlight");
    }
}
