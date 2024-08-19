document.addEventListener('DOMContentLoaded', () => {
    function loadQuestion() {
        return fetch('/get-question')
            .then(response => response.json())
            .then(data => {
                flashcard_container = document.getElementById('flashcard-container');
                flashcard_container.innerHTML = "";
                data.question.split("\n").forEach(line => {
                    flashcard_container.appendChild(document.createTextNode(line))
                    flashcard_container.appendChild(document.createElement("br"))
                });
                document.getElementById('submit-answer').onclick = () => submitAnswer(data);
            });
    }

    function setTheoryMode() {
        var modeSelection = document.getElementById("theory-mode").value;
        return fetch(`/set-theory-mode/${modeSelection}`, {method: 'GET'});
    }

    function fillConfigOptions() {
        var modeSelection = document.getElementById("theory-mode").value;
        return fetch(`/get-configs/${modeSelection}`, {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            cfg_dropdown_ele = document.getElementById("config");
            cfg_dropdown_ele.length = 0;
            data.forEach(element => {
                var option = document.createElement('option');
                option.text = option.value = element
                cfg_dropdown_ele.options.add(option)
            });
        });
    }

    function loadConfig() {
        var configSelection = document.getElementById("config").value;
        return fetch(`/load-config/${configSelection}`, {method: 'GET'});
    }

    async function theoryModeInit() {
        await setTheoryMode();
        await fillConfigOptions();
        await loadConfig();
        await loadQuestion();
    }

    async function configInit() {
        await loadConfig();
        await loadQuestion();
    }

    function submitAnswer(questionData) {
        const guess = document.getElementById('answer-input').value;
        return fetch('/submit-answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ guess: guess, answer: questionData.answer })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.feedback)
            document.getElementById('correct').innerText = `Correct: ${data.correct}`
            document.getElementById('total').innerText = `Total: ${data.total}`
            var percent = Math.round((data.correct / data.total) * 100)
            document.getElementById('percentage').innerText = `${percent}% Correct`
            loadQuestion();
        });
    }

    theoryModeInit()
    document.getElementById('theory-mode').onchange = theoryModeInit;
    document.getElementById('config').onchange = configInit;
});
