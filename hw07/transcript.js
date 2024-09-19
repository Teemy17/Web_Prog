document.addEventListener("DOMContentLoaded", () => {
    function updateTranscriptTable(transcriptData) {
        const contentBody = document.getElementById("content_body");
        contentBody.innerHTML = ""; // Clear existing content

        let totalCreditsAttempted = 0;
        let totalPointsEarned = 0;

        Object.entries(transcriptData.credit).forEach(([year, semesters]) => {
            Object.entries(semesters).forEach(([semester, courses]) => {
                // Create and append semester label row
                const semesterLabelRow = document.createElement("tr");
                const semesterLabelCell = document.createElement("td");
                semesterLabelCell.textContent = `${semester}, ${year}`;
                semesterLabelCell.style.textDecoration = "underline", semesterLabelCell.style.fontWeight = "bold";
                semesterLabelRow.appendChild(semesterLabelCell);
                semesterLabelRow.appendChild(document.createElement("td"));
                semesterLabelRow.appendChild(document.createElement("td"));
                contentBody.appendChild(semesterLabelRow);

                let semesterCreditsAttempted = 0;
                let semesterPointsEarned = 0;

                courses.forEach(course => {
                    const row = document.createElement("tr");

                    // Add course details
                    row.innerHTML = `
                        <td style="text-align: left">${course.subject_id} ${course.name}</td>
                        <td>${course.credit}</td>
                        <td>${course.grade}</td>
                    `;
                    contentBody.appendChild(row);

                    const gradePoints = {
                        "A": 4.0,
                        "B+": 3.5,
                        "B": 3.0,
                        "C+": 2.5,
                        "C": 2.0,
                        "D+": 1.5,
                        "D": 1.0
                    };
                    const gradePoint = gradePoints[course.grade] || 0;

                    if (gradePoint > 0) {
                        const credits = parseFloat(course.credit);
                        semesterCreditsAttempted += credits;
                        semesterPointsEarned += credits * gradePoint;
                    }
                });

                // Calculate and display semester GPA
                if (semesterCreditsAttempted > 0) {
                    const semesterGPA = semesterPointsEarned / semesterCreditsAttempted;
                    totalCreditsAttempted += semesterCreditsAttempted;
                    totalPointsEarned += semesterPointsEarned;
                    const overallGPA = totalPointsEarned / totalCreditsAttempted;

                    const semesterGPSText = `GPS: ${semesterGPA.toFixed(2)}  GPA: ${overallGPA.toFixed(2)}`;
                    const semesterGPSRow = document.createElement("tr");
                    const semesterGPSCell = document.createElement("td");
                    semesterGPSCell.textContent = semesterGPSText;
                    semesterGPSCell.style.fontStyle = "italic";
                    semesterGPSRow.appendChild(semesterGPSCell);
                    semesterGPSRow.appendChild(document.createElement("td"));
                    semesterGPSRow.appendChild(document.createElement("td"));
                    contentBody.appendChild(semesterGPSRow);
                }
            });
        });

        // Populate student information
        document.getElementById("student_name").value = transcriptData.student_name;
        document.getElementById("date_of_birth").value = transcriptData.date_of_birth;
        document.getElementById("student_id").value = transcriptData.student_id;
        document.getElementById("date_of_admission").value = transcriptData.date_of_admission;
        document.getElementById("date_of_graduation").value = transcriptData.date_of_graduation;
        document.getElementById("degree").value = transcriptData.degree;
        document.getElementById("major").value = transcriptData.major;
    }

    // Function to handle file input change
    function handleFileInputChange(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const jsonData = JSON.parse(e.target.result);
                    updateTranscriptTable(jsonData);
                } catch (error) {
                    alert("Error parsing JSON file: " + error.message);
                }
            };
            reader.readAsText(file);
        }
    }

    // Attach the file input change event handler
    document.getElementById("fileInput").addEventListener("change", handleFileInputChange);
});
