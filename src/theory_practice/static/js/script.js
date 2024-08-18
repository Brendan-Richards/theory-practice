document.addEventListener('DOMContentLoaded', () => {
    function loadQuestion() {
        fetch('/get-question')
            .then(response => response.json())
            .then(data => {
                document.getElementById('flashcard').textContent = generateQuestionText(data);
                document.getElementById('submit-answer').onclick = () => submitAnswer(data);
                document.getElementById('theory-mode').onchange = () => fillConfigOptions(data);
            });
    }

    function generateQuestionText(data) {
        // print("in generateQuestionText", data)
        return "question text 2"
        // if (data.type === 'Interval') {
        //     return `Root: ${data.root}\nInterval: ${data.interval}\nDirection: ${data.direction === 'a' ? 'Ascending' : 'Descending'}`;
        // }
        // Add more cases for other types
    }

    function submitAnswer(questionData) {
        const guess = document.getElementById('answer-input').value;
        fetch('/submit-answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ guess: guess, question_data: questionData })
        })
            .then(response => response.json())
            .then(data => {
                if (data.correct) {
                    alert('Correct!');
                } else {
                    alert('Incorrect!');
                }
                loadQuestion();
            });
    }

    function fillConfigOptions() {
        // fetch('/get-configs')
        // .then(response => response.json())
        // .then(data => {
        //     // var select = document.getElementById("year");
        //     alert(data)

        //     // document.getElementById('flashcard').textContent = generateQuestionText(data);
        //     // document.getElementById('submit-answer').onclick = () => submitAnswer(data);
        // });
        
        var modeSelection = document.getElementById("theory-mode").value;
        alert("filling config options");
        alert(modeSelection);

        fetch(`/get-configs/${modeSelection}`, {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            alert(data)
        });
        
    }

    fillConfigOptions();
    loadQuestion();
});
