# 🍷 Wine Quality Checker

This project is a full-stack web application that predicts the quality of red wine based on lab test parameters. It allows users to either manually input lab values or upload a PDF report, from which the application extracts data using **Groq's LLaMA 3.1** language model API. The prediction is performed by a trained machine learning model served through a **FastAPI** backend, while the frontend is built using **React.js**.

---

## ✨ Features

- 📄 **Upload Lab Reports (PDF)**
  - Automatically extract key wine parameters using Groq LLaMA 3.1
- ✍️ **Manual Form Input**
  - Enter lab values if no report is available
- 🤖 **ML Prediction**
  - Predicts wine quality score and its classification
- 🔗 **Full Stack App**
  - React + FastAPI + ML Model + Groq API

---

## 🏗️ Tech Stack

| Layer        | Tech Used                     |
|--------------|-------------------------------|
| Frontend     | React.js                      |
| Backend      | FastAPI                       |
| LLM API      | Groq (LLaMA 3.1)              |
| ML Model     | Trained on Wine Quality Dataset |
| File Parsing | PyMuPDF (PDF to text)         |
| Styling      | Custom CSS                    |

---

## 📊 Wine Quality Prediction

The prediction model uses chemical and physical wine attributes such as:

- Fixed Acidity
- Volatile Acidity
- Citric Acid
- Residual Sugar
- Chlorides
- Free Sulfur Dioxide
- Total Sulfur Dioxide
- Density
- pH
- Sulphates
- Alcohol

A trained classifier returns:
- Predicted Quality Score (0–10)
- Class (e.g., Low, Medium, High)

---

## 🔑 Groq + LLaMA 3.1

The app uses the **Groq API** to run the **LLaMA 3.1 language model**, which is responsible for:

> "Extracting structured lab data from raw PDF lab reports in natural language form."

### Example Output:
```json
{
  "fixed_acidity": "7.4",
  "volatile_acidity": "0.70",
  "citric_acid": "0.00",
  ...
}





🚀 How to Run the Project
1. Clone the Repository
git clone https://github.com/OjasavDobhal/Wine-quality-check.git
cd Wine-quality-check

2. Setup Environment
Backend Setup (FastAPI)

cd backend
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt
Create .env file in backend/ folder:GROQ_API_KEY=your_groq_api_key

uvicorn main:app --reload

Frontend Setup (React)

cd frontend
npm install
npm start

📂 Project Structure

Wine-quality-check/
├── backend/
│   ├── main.py                # FastAPI app
│   ├── model.pkl              # Trained ML model
│   ├── extractor.py           # PDF to text + Groq logic
│   ├── requirements.txt
│   └── .env                   # Contains GROQ_API_KEY
├── frontend/
│   ├── src/
│   │   ├── PredictionForm.js  # Main form UI
│   │   ├── App.js
│   │   └── index.css
│   └── package.json
└── README.md


Made with ❤️ by Ojasav Dobhal
