document.addEventListener("DOMContentLoaded", () => {
    console.log("JS Loaded");

    //TEXT INPUT
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

    //MIC INPUT
    let mediaRecorder;
    let audioChunks = [];

    const startBtn = document.getElementById("startRecording");
    const stopBtn = document.getElementById("stopRecording");

    if (startBtn && stopBtn) {

        startBtn.addEventListener("click", async () => {

            let stream;
            try {
                stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            } catch (err) {
                alert("Microphone permission denied or not working");
                return;
            }

            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.start();

            document.getElementById("recordingStatus").innerText = "Recording...";
        });

        stopBtn.addEventListener("click", () => {

            if (!mediaRecorder) return;
            mediaRecorder.stop();

            mediaRecorder.onstop = () => {

                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

                const formData = new FormData();
                formData.append("audio", audioBlob, "recording.wav");

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

                    document.getElementById("recordingStatus").innerText = "Done!";
                });
            };
        });
    }
});