let currentQuestion = 1;
const serverUrl = 'http://172.16.13.244:5000';
function nextQuestion() {
    const currentQuestionElement = document.getElementById(`question${currentQuestion}`);
    const nextQuestionElement = document.getElementById(`question${currentQuestion + 1}`);

    if (currentQuestionElement && nextQuestionElement) {
        currentQuestionElement.style.display = 'none';
        nextQuestionElement.style.display = 'block';
        currentQuestion++;
    }
}

function updateAgeValue() {
    var ageInput = document.getElementById("ageInput");
    var ageValue = document.getElementById("ageValue");
    ageValue.textContent = ageInput.value;
}



function submitForm() {
    var km = document.getElementById("temp");
    km.textContent = 'We are trying to find out your disease ............'

    const symptoms = document.querySelectorAll('input[name="symptoms[]"]:checked');

    const selectedSymptoms = Array.from(symptoms).map(checkbox => {
        const label = document.querySelector(`label[for="${checkbox.id}"]`);
        return label.textContent.trim();
    });
    // Log the selected symptoms to the console
    console.log("Selected Symptoms:", selectedSymptoms);

    alert("Form submitted successfully!");

    fetch(`${serverUrl}/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symptoms: selectedSymptoms }),
    })
        .then(response => response.json())
        .then(data => {
            // Process the results returned from the backend
            console.log(data);

            const chartContainer = document.getElementById('chartContainer');
            chartContainer.innerHTML = '';  // Clear previous content

            console.log("YUP")
            if (data.top_diseases && data.probabilities) {
                const chartImg = document.createElement('img');
                chartImg.src = `data:image/png;base64,${data.image_data}`;
                chartContainer.appendChild(chartImg);
            } else {
                // If no data is provided, you can handle it as needed
                console.log("NOPS")
                const placeholderText = document.createElement('p');
                placeholderText.textContent = 'No data available';
                chartContainer.appendChild(placeholderText);
            }
            km.textContent = '';
        })

}