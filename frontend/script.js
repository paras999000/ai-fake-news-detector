document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const newsInput = document.getElementById('news-input');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const spinner = analyzeBtn.querySelector('.spinner');
    
    const resultCard = document.getElementById('result-card');
    const predictionLabel = document.getElementById('prediction-label');
    const trustScore = document.getElementById('trust-score');
    const meterBar = document.getElementById('meter-bar');
    const explanationText = document.getElementById('explanation-text');
    const errorMessage = document.getElementById('error-message');

    // API URL - Change this if you deploy the backend
    const API_URL = 'http://localhost:8000/analyze';

    analyzeBtn.addEventListener('click', async () => {
        const text = newsInput.value.trim();
        
        if (!text) {
            // Slight shake animation or alert if empty
            newsInput.style.transform = 'translate(-5px, 0)';
            setTimeout(() => newsInput.style.transform = 'translate(5px, 0)', 100);
            setTimeout(() => newsInput.style.transform = 'translate(0, 0)', 200);
            return;
        }

        // Set Loading State
        analyzeBtn.disabled = true;
        btnText.textContent = 'Analyzing...';
        spinner.classList.remove('hidden');
        resultCard.classList.add('hidden');
        errorMessage.classList.add('hidden');
        
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                throw new Error('Server responded with an error.');
            }

            const data = await response.json();
            displayResult(data);

        } catch (error) {
            console.error('Error calling the API:', error);
            errorMessage.classList.remove('hidden');
        } finally {
            // Reset Loading State
            analyzeBtn.disabled = false;
            btnText.textContent = 'Check News';
            spinner.classList.add('hidden');
        }
    });

    function displayResult(data) {
        // Remove previous status classes
        resultCard.classList.remove('status-real', 'status-fake');
        
        // Add new class based on prediction
        if (data.is_real) {
            resultCard.classList.add('status-real');
        } else {
            resultCard.classList.add('status-fake');
        }

        predictionLabel.textContent = data.prediction_label;
        trustScore.textContent = `${data.trust_score}%`;
        
        // Reset meter to 0 first to trigger animation
        meterBar.style.width = '0%';
        
        // Show the result card
        resultCard.classList.remove('hidden');
        
        // Use a slight delay to allow the DOM to render before animating the bar
        setTimeout(() => {
            meterBar.style.width = `${data.trust_score}%`;
        }, 50);

        explanationText.textContent = data.explanation;
    }
});
