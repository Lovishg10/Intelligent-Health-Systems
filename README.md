# 🏥 HealthCenter AI: Intelligent Hospital Management System
### *Pravega x NPCI Innovation Hackathon 2026 Submission*

**Designed and implemented with ❤️ and passion by Lovish Garg**

*Team: Code Blue (Solo Developer)*

---

## 🌟 Project Overview
HealthCenter AI is a streamlined digital ecosystem built to organize hospital workflows. It replaces manual paperwork with a digital pipeline for patients, doctors, and administrators, ensuring that hospital operations stay clear and manageable.

## 🛡️ Key Feature: Manual Risk-Check for Doctors
To assist doctors in high-pressure environments, the system includes a dedicated **Risks** button within the prescription interface:
* **Doctor-Led Validation**: The doctor can proactively click the Risks button to get instant precautions.
* **Safety Insights**: It flags potential side effects or contraindications, acting as a quick digital reference to help manage risks before finalizing a prescription.

## 🏗️ Technical Resilience: 3-Layer Failover
The system is built to stay online even if the primary cloud service fails, using a hierarchical logic:
1. **Primary**: Google Gemini 2.0 Flash for fast, intelligent reasoning.
2. **Secondary**: Llama 3.1 (via local inference) if the internet/API is unstable.
3. **Tertiary**: A local Rule Engine to ensure basic dashboard functionality and data entry never stop.

## ✨ Core Functionalities
* **Automated Triage**: AI-assisted sorting to speed up patient registration at the front desk.
* **Doctor Dashboard**: A clean, real-time queue to manage active and treated patients effortlessly.
* **Live Admin Analytics**: Real-time charts showing department loads, helping admins deploy staff where they are needed most.
* **Digital History**: Every visit generates a digital record, so patients never lose their dosage instructions or prescriptions.

## 🛠️ Tech Stack
* **Frontend/UI**: Streamlit (Python)
* **AI Models**: Google Gemini 1.5 Flash & Llama 3.1
* **Backend**: Python
* **Architecture**: 3-Layer Failover Logic

---
## ⚙️ Installation & Setup

### 1. Clone the Repository
```
git clone https://github.com/Lovishg10/Intelligent-Health-Systems.git
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. API Configurations
The system requires two API keys to handle the Dual-Model Failover logic. Create a .env file in the same directory as main.py and add your API keys:

```
GOOGLE_API_KEY=your_gemini_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```
### 4. Running the Program
In the CLI , enter command
```
streamlit run main.py
```
---

> "Scalable. Reliable. Life-Saving."

