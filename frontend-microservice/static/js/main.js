document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const imagePreview = document.getElementById('imagePreview');
    const uploadIcon = document.getElementById('uploadIcon');
    const error = document.getElementById('error');
    const results = document.getElementById('results');

    // Handle drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFile(file);
        }
    });

    // Handle click upload
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    function handleFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove('hidden');
            uploadIcon.classList.add('hidden');
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // Handle form submission
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        error.classList.add('hidden');
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Processing...';

        const formData = new FormData(uploadForm);

        try {
            // First API call
            const predictionResponse = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const predictionData = await predictionResponse.json();

            if (predictionData.error) {
                throw new Error(predictionData.error);
            }

            displayPredictionResults(predictionData.prediction);

            // Second API call
            const biogptResponse = await fetch('/biogpt', {
                method: 'POST'
            });
            const biogptData = await biogptResponse.json();

            if (biogptData.error) {
                throw new Error(biogptData.error);
            }

            displayBioGPTResults(biogptData.biogpt);
            results.classList.remove('hidden');
        } catch (err) {
            error.textContent = err.message;
            error.classList.remove('hidden');
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze Image';
        }
    });

    function displayPredictionResults(prediction) {
        const cards = document.querySelectorAll('.prediction-card');
        const models = ['DenseNet', 'EfficientNet', 'ResNet'];

        models.forEach((model, index) => {
            const confidence = prediction[`${model}_Confidence`] * 100;
            cards[index].querySelector('.prediction').textContent = prediction[`${model}_Predict`];
            cards[index].querySelector('.confidence').textContent = `Confidence: ${confidence.toFixed(2)}%`;
        });

        document.getElementById('finalPrediction').textContent = prediction.Final_Predict;
        document.querySelector('.biogpt-results').classList.add('hidden');
    }

    function displayBioGPTResults(data) {
        document.getElementById('definition').textContent = data.definition;
        document.getElementById('dangerLevel').textContent = data.danger_level;
        document.getElementById('symptoms').textContent = data.symptoms;
        document.getElementById('causes').textContent = data.causes;
        document.getElementById('riskFactors').textContent = data.risk_factors;
        document.getElementById('survivalRate').textContent = data.survival_rate;
        document.getElementById('diagnosisMethods').textContent = data.diagnosis_methods;
        document.getElementById('treatmentOptions').textContent = data.treatment_options;
        document.getElementById('recommendedActions').textContent = data.what_we_need_to_do;

        document.querySelector('.biogpt-results').classList.remove('hidden');
    }
});