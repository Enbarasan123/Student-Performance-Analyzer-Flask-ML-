# 🎓 Student Performance Analyzer (Flask + ML)

A smart web-based application built using **Flask**, **Machine Learning**, and **SQLite** to analyze student performance, predict scores, and provide personalized study plans.

---

## 🚀 Features

* 🔐 User Authentication (Login system)
* 📊 Student Marks Management
* 🤖 ML-based Score Prediction (Linear Regression)
* 📈 Performance Analysis (Pass/Fail)
* 📚 Personalized Study Plan Generator
* 💡 Smart Suggestions based on performance
* 🏆 Leaderboard with filtering (Pass/Fail)
* 🔍 Search functionality
* 📄 Export student report as PDF

---

## 🧠 Machine Learning

The app uses **Linear Regression (sklearn)** to predict total scores based on subject marks.

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite
* **Machine Learning:** Scikit-learn, NumPy
* **PDF Generation:** ReportLab
* **Frontend:** HTML (Jinja Templates)

---

## 📁 Project Structure

```
project/
│── app.py
│── database.db
│── templates/
│   ├── login.html
│   ├── dashboard.html
│── static/
│── report.pdf (generated)
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/student-performance-analyzer.git
cd student-performance-analyzer
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies

```bash
pip install flask numpy scikit-learn reportlab
```

*(Using requirements.txt is a common practice in Flask projects)* ([GitHub][1])

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

```
http://127.0.0.1:5000/
```

---

## 🔑 Default Login

```
Username: admin
Password: admin
```

---

## 📊 Functional Overview

### 🔹 Prediction

* Uses ML model to predict total marks

### 🔹 Study Plan

* Generates daily study hours based on subject performance

### 🔹 Suggestions

* Highlights weak, average, and strong subjects

### 🔹 Leaderboard

* Ranks students based on total marks

---

## 📄 Export Feature

* Download all student data as a **PDF report**

---

## 🧩 Future Improvements

* Add charts/visualizations
* Use advanced ML models
* Role-based login system
* Deploy on cloud (Render / Heroku)

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit a pull request.

---


## 👨‍💻 Author

**Enbarasan**

---

