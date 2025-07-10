<h1 align="center"> 🏊‍♂️ Swimmer Performance Analysis </h1>


Welcome to the Swimmer Performance Analyzer – a web-based application designed to analyze swimmer performance data, visualize key metrics, and provide personalized recommendations for improvement.

> 📦 Note: This project contains large data files. They are compressed into swimmer_data.zip for easier download and to keep the repository lightweight. Be sure to extract this zip file to access the data.


## 🚀 Project Overview

This tool is ideal for swimmers, coaches, and performance analysts. By processing raw lap time data, it offers valuable insights into trends, pacing, consistency, and predicts future race outcomes. The analysis is presented via an interactive web interface.


## ✨ Features

* 📂 Data Processing
Automatically extracts swimmer info (name, age, distance, stroke, lap times) from .txt files.

* 📊 Performance Metrics
Calculates key statistics like total race time, average lap time, velocity, and estimated heart rate.

* 📈 Visualizations

   • Total Race Times: Tracks a swimmer’s race performance over time.

   • Average Lap Times by Distance & Stroke: Pinpoints areas for improvement based on lap analysis.

* 🔮 Performance Prediction
Uses linear regression to predict a swimmer's next race time.

* 💡 Personalized Recommendations
Actionable feedback based on lap time consistency, velocity trends, and heart rate analysis.

* 🌐 Web Interface
A clean Flask-powered web UI for displaying results and plots.


## ⚙️ How It Works

1️⃣ Data Ingestion

The process_files() function scans for .txt files named like SwimmerName-Age-DistanceStroke.txt (e.g., JohnDoe-18-100mFreestyle.txt) and reads lap times in minutes:seconds format.

2️⃣ Data Analysis
* parse_time(): Converts time to seconds

* calculate_velocity(): Computes speed

* analyze_swimmer():

* Filters swimmer-specific data

* Computes performance metrics

* Generates plots

* Predicts race time using linear regression

* Estimates heart rate

* Outputs personalized tips

3️⃣ Web Interface
* The app uses Flask to serve a web UI (index.html)

* Data is fetched via the /swimmer/<name> route and returned as a JSON response with:

   • Total Race Times: Tracks a swimmer’s race performance over time.
Base64-encoded plots

   • Total Race Times: Tracks a swimmer’s race performance over time.
Metrics and suggestions

## 🗂️ Repository Structure

      Swimmer_Performance_Analyzer/
      │
      ├── app.py                # Flask application
      ├── swimmer_data.zip      # Compressed swimmer .txt data files
      ├── .gitattributes
      ├── README.md
      └── templates/
          └── index.html        # Web interface template

## 🔧 Getting Started

* ✅ Prerequisites
Ensure Python 3.7+ is installed. Then install the required packages:

    pip install Flask pandas matplotlib scikit-learn numpy

* ▶️ Running the App
1. Extract the Data

   Unzip swimmer_data.zip into the same folder as app.py.

2. Navigate to the Project Folder

        cd Swimmer_Performance_Analyzer

3. Start the Flask App

        python app.py

4. Open in Browser

   Visit http://127.0.0.1:5000/ to access the main UI.

   For swimmer-specific analysis:

          http://127.0.0.1:5000/swimmer/JohnDoe


## 🧪 Technologies Used
* Python (3.7+)

* Flask – Web framework

* Pandas – Data processing

* Matplotlib – Plotting

* NumPy – Numeric operations

* Scikit-learn – Regression analysis


## 🧠 How to Interact

Once the app is live, you can:

   * Enter a swimmer’s name via the UI (if input is provided in index.html)

   * Or access /swimmer/<SwimmerName> directly

You'll get:

* 📊 Performance visualizations

* 🔢 Key stats (lap times, speed, predicted time, heart rate)

* 💬 Personalized improvement tips


## 📌 Future Improvements

* Add swimmer profile uploads via the web UI

* Support video-based stroke analysis (via ML/CV)

* Store swimmer history in a database

* Enable login & personalized dashboards



## 📬 Contact
Feel free to reach out for suggestions or collaboration ideas!

