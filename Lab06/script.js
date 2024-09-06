function calculateBMI() {
    // Get user inputs
    const weight = parseFloat(document.getElementById("weight").value);
    const height = parseFloat(document.getElementById("height").value);
    const heightM = height / 100;
    const bmiResultDiv = document.getElementById("bmiResult");

    // Calculate BMI
    const bmi = weight / (heightM * heightM);
    const bmiOutput = document.getElementById("bmiOutput");

    // Display BMI result
    bmiOutput.innerText = ` With your weight of ${weight} Kg and height of ${height} cm.
    Your BMI is: ${bmi.toFixed(2)}`;
    bmiResultDiv.style.display = "block";


    if (bmi < 18.5) {
    document.getElementById("underweight");
    } else if (bmi >= 18.5 && bmi <= 24.9) {
    document.getElementById("normal");
    } else if (bmi >= 25 && bmi <= 29.9) {
    document.getElementById("overweight");
    } else {
    document.getElementById("obese");
    }
}
