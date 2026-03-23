document.addEventListener("DOMContentLoaded", () => {
    console.log("JS Loaded");

    const sendButton = document.getElementById("submitAnswer");

    if (sendButton) {
        sendButton.addEventListener("click", () => {

            const textarea = document.getElementById("userAnswer");
            const answer = textarea.value;

            if (!answer) {
                alert("Please enter an answer");
                return;
            }

            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ answer: answer }),
            })
            .then(response => response.json())
            .then(data => {
                console.log("Response from backend:", data);

                document.getElementById("scoreDisplay").innerText =
                    "Score: " + data.accuracy_score + " | Total: " + data.total_score;

                document.getElementById("feedbackDisplay").innerText =
                    "Feedback: " + data.feedback;

                // document.getElementById("nextQuestionDisplay").innerText =
                //     "Next Question: " + data.next_question;

                document.getElementById("questionDisplay").innerText = 
                    data.next_question;
            })
            .catch(error => {
                console.error("Error:", error);
            });

        });
    }
    //Audio
    const uploadBtn = document.getElementById("uploadAudio");

    if (uploadBtn) {
        uploadBtn.addEventListener("click", () => {

            const fileInput = document.getElementById("audioInput");
            const file = fileInput.files[0];

            if (!file) {
                alert("Please select audio file");
                return;
            }

            const formData = new FormData();
            formData.append("audio", file);

            fetch('/upload_audio', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("scoreDisplay").innerText =
                    "Score: " + data.accuracy_score + " | Total: " + data.total_score;

                document.getElementById("feedbackDisplay").innerText =
                    "Feedback: " + data.feedback;

                document.getElementById("questionDisplay").innerText =
                    data.next_question;
            });
        });
    }
});