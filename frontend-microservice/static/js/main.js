document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const imagePreview = document.getElementById('imagePreview');
    const uploadIcon = document.getElementById('uploadIcon');
    const error = document.getElementById('error');
    const analysisSection = document.getElementById('analysisSection');
    
    // Navigation Buttons
    const homeBtn = document.getElementById('homeBtn');
    const analyzeBtnNav = document.getElementById('analyzeBtnNav');
    const monitoringBtn = document.getElementById('monitoringBtn');
    
    // Sections
    const homeSection = document.getElementById('homeSection');
    const analyzeSection = document.getElementById('analyzeSection');

    
    // Show and hide sections
    function showSection(sectionToShow) {
        [homeSection, analyzeSection, analysisSection].forEach(section => {
            section.classList.add('hidden'); // Hide all sections, including analysisSection
        });
        sectionToShow.classList.remove('hidden'); // Show the selected section
    }
    

    homeBtn.addEventListener('click', () => showSection(homeSection));
    analyzeBtnNav.addEventListener('click', () => showSection(analyzeSection));
    monitoringBtn.addEventListener("click", async function () {
        try {
            const res = await fetch("/get-monitoring-url");
            const url = await res.text(); // Get plain text
            window.location.href = url; // Redirect in same tab
        } catch (err) {
            console.error("Failed to fetch monitoring URL:", err);
        }
    });
    
    // ✅ Redirects to monitoring dashboard

    // Drag & Drop Upload
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFile(file);
        }
    });

    // Click to Upload
    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
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

    // Form Submission (API Calls)
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        error.classList.add('hidden');
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Processing...';

        const formData = new FormData(uploadForm);

        try {
            // Prediction API Call
            const predictionResponse = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const predictionData = await predictionResponse.json();

            if (predictionData.error) throw new Error(predictionData.error);

            displayPredictionResults(predictionData.prediction);

            // BioGPT API Call
            const biogptResponse = await fetch('/biogpt', { method: 'POST' });
            const biogptData = await biogptResponse.json();

            if (biogptData.error) throw new Error(biogptData.error);

            displayBioGPTResults(biogptData.biogpt);

            // Show analysis results
            analysisSection.classList.remove('hidden');
        } catch (err) {
            error.textContent = err.message;
            error.classList.remove('hidden');
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze Image';
        }
    });

    function displayPredictionResults(prediction) {
        const models = ['DenseNet', 'EfficientNet', 'ResNet'];
        const predictionCards = document.querySelectorAll('.prediction-card');

        models.forEach((model, index) => {
            const confidence = prediction[`${model}_Confidence`] * 100;
            predictionCards[index].querySelector('.prediction').textContent = prediction[`${model}_Predict`];
            predictionCards[index].querySelector('.confidence').textContent = `Confidence: ${confidence.toFixed(2)}%`;
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
