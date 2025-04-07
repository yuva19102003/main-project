from flask import Flask, jsonify, request
import random

data = {
    "normal_lung": {
        "1": {
            "definition": "Lungs appear normal, no abnormalities.",
            "symptoms": "Clear breathing, no cough",
            "causes": "Healthy lifestyle",
            "what_we_need_to_do": "Maintain healthy diet",
            "danger_level": "Low",
            "diagnosis_methods": "X-rays, CT scans",
            "treatment_options": "Not required",
            "risk_factors": "Good air quality",
            "survival_rate": "100%"
        },
        "2": {
            "definition": "Healthy lung function, no diseases.",
            "symptoms": "Normal oxygen levels",
            "causes": "No exposure to pollutants",
            "what_we_need_to_do": "Avoid smoking",
            "danger_level": "Low",
            "diagnosis_methods": "Routine checkups",
            "treatment_options": "Regular exercise",
            "risk_factors": "No smoking, clean environment",
            "survival_rate": "100%"
        },
        "3": {
            "definition": "Optimal lung condition, no issues.",
            "symptoms": "No shortness of breath",
            "causes": "No infection or inflammation",
            "what_we_need_to_do": "Exercise regularly",
            "danger_level": "Low",
            "diagnosis_methods": "Annual checkups",
            "treatment_options": "Deep breathing exercises",
            "risk_factors": "Active lifestyle",
            "survival_rate": "100%"
        },
        "4": {
            "definition": "No signs of inflammation or infection.",
            "symptoms": "Strong lung capacity",
            "causes": "Good immune response",
            "what_we_need_to_do": "Improve lung endurance",
            "danger_level": "Low",
            "diagnosis_methods": "Oxygen tests",
            "treatment_options": "Healthy diet, cardio workouts",
            "risk_factors": "Proper ventilation",
            "survival_rate": "100%"
        },
        "5": {
            "definition": "Perfect lung capacity, smooth breathing.",
            "symptoms": "Full oxygen saturation levels",
            "causes": "No genetic disorders",
            "what_we_need_to_do": "Routine exercise",
            "danger_level": "Low",
            "diagnosis_methods": "Spirometry tests",
            "treatment_options": "Yoga, aerobic exercises",
            "risk_factors": "No history of lung disease",
            "survival_rate": "100%"
        }
    },
    "squamous_carcinoma": {
        "1": {
            "definition": "Squamous cell carcinoma, lung cells affected.",
            "symptoms": "Chronic cough, coughing blood, fatigue",
            "causes": "Heavy smoking",
            "what_we_need_to_do": "Immediate consultation",
            "danger_level": "Very High",
            "diagnosis_methods": "X-ray, bronchoscopy",
            "treatment_options": "Radiation, chemotherapy",
            "risk_factors": "Smoking, occupational hazards",
            "survival_rate": "20-40%"
        },
        "2": {
            "definition": "Aggressive squamous carcinoma.",
            "symptoms": "Hoarseness, weight loss",
            "causes": "Smoking, alcohol",
            "what_we_need_to_do": "Urgent intervention",
            "danger_level": "Critical",
            "diagnosis_methods": "Biopsy, PET scan",
            "treatment_options": "Advanced chemotherapy",
            "risk_factors": "Heavy tobacco use",
            "survival_rate": "5-15%"
        },
        "3": {
            "definition": "Advanced squamous cell carcinoma.",
            "symptoms": "Severe chest pain, difficulty swallowing",
            "causes": "Asbestos exposure",
            "what_we_need_to_do": "Urgent hospitalization",
            "danger_level": "Critical",
            "diagnosis_methods": "PET scan, biopsy",
            "treatment_options": "Palliative care, radiation",
            "risk_factors": "Industrial exposure",
            "survival_rate": "5-10%"
        },
        "4": {
            "definition": "Squamous carcinoma, slow progression.",
            "symptoms": "Coughing up mucus, chest congestion",
            "causes": "Pollutants",
            "what_we_need_to_do": "Lifestyle changes",
            "danger_level": "High",
            "diagnosis_methods": "CT scan, X-rays",
            "treatment_options": "Surgery, therapy",
            "risk_factors": "Second-hand smoke exposure",
            "survival_rate": "25-35%"
        },
        "5": {
            "definition": "Squamous carcinoma, secondary infections.",
            "symptoms": "Hoarseness, breathing pain",
            "causes": "Weakened immunity",
            "what_we_need_to_do": "Complex treatment",
            "danger_level": "Very High",
            "diagnosis_methods": "Genetic screening",
            "treatment_options": "Multi-stage radiation",
            "risk_factors": "Family history of cancer",
            "survival_rate": "10-20%"
        }
    },
    "adenocarcinoma": {
        "1": {
            "definition": "Adenocarcinoma, a lung cancer subtype.",
            "symptoms": "Cough, weight loss, fatigue",
            "causes": "Smoking, pollution",
            "what_we_need_to_do": "Biopsy, consult a doctor",
            "danger_level": "High",
            "diagnosis_methods": "CT, PET scans, biopsy",
            "treatment_options": "Surgery, chemotherapy",
            "risk_factors": "Smoking, air pollution",
            "survival_rate": "15-30%"
        },
        "2": {
            "definition": "Lung adenocarcinoma, peripheral lungs.",
            "symptoms": "Shortness of breath, fatigue",
            "causes": "Air pollution",
            "what_we_need_to_do": "Early screening",
            "danger_level": "Moderate",
            "diagnosis_methods": "CT scan, blood tests",
            "treatment_options": "Targeted drug therapy",
            "risk_factors": "Airborne carcinogens",
            "survival_rate": "25-40%"
        },
        "3": {
            "definition": "Late-stage adenocarcinoma, metastasis.",
            "symptoms": "Severe weight loss, breathing issues",
            "causes": "Smoking history",
            "what_we_need_to_do": "Aggressive treatment",
            "danger_level": "Very High",
            "diagnosis_methods": "Biopsy, gene testing",
            "treatment_options": "Targeted therapy",
            "risk_factors": "Chronic smoking habits",
            "survival_rate": "5-15%"
        },
        "4": {
            "definition": "Intermediate-stage adenocarcinoma.",
            "symptoms": "Frequent lung infections, cough",
            "causes": "Chemical exposure",
            "what_we_need_to_do": "Specialized care",
            "danger_level": "High",
            "diagnosis_methods": "CT scan, PET scan",
            "treatment_options": "Radiation, chemotherapy",
            "risk_factors": "Workplace exposure",
            "survival_rate": "15-25%"
        },
        "5": {
            "definition": "Early-stage adenocarcinoma detected.",
            "symptoms": "Mild cough, occasional wheezing",
            "causes": "Passive smoking",
            "what_we_need_to_do": "Early intervention",
            "danger_level": "Moderate",
            "diagnosis_methods": "Low-dose CT scan",
            "treatment_options": "Surgery if operable",
            "risk_factors": "Passive smoking exposure",
            "survival_rate": "40-50%"
        }
    }
}

# choosing the name
def get_name(section):
    if section == "Normal lung":
        return "normal_lung"
    elif section == "Squamous cell carcinoma":
        return "squamous_carcinoma"
    elif section == "Lung adenocarcinoma":
        return "adenocarcinoma"
    else:
        return "normal_lung"


# Function to choose a random number
def get_random_number():
    return random.choice([1, 2, 3, 4, 5])

# Function to get data from the dataset
def fetch_data(name, key):
    return data.get(name, {}).get(key, "No data found")

app = Flask(__name__)

@app.route('/biogpt', methods=['GET'])
def get_data():
    request_data = request.get_json()
    section = request_data.get("name", "")
    name = get_name(section)
    response = fetch_data(name, str(get_random_number()))
    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
