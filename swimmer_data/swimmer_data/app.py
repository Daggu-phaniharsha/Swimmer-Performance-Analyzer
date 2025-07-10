import matplotlib
matplotlib.use('Agg')

import os
from flask import Flask, request, jsonify, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

def parse_time(time_str):
    try:
        minutes, seconds = map(float, time_str.split(':'))
        return minutes * 60 + seconds
    except ValueError:
        print(f"Error parsing time string: '{time_str}'")
        return 0

def process_files(directory="."):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            parts = filename.split("-")
            swimmer_name = parts[0]
            age = int(parts[1])
            distance_stroke = parts[2] + "-" + parts[3].split(".")[0]
            distance, stroke = distance_stroke.split("-")
            with open(filename, "r") as file:
                times = file.read().strip().split(",")
                lap_times = [parse_time(t) for t in times]
                total_time = sum(lap_times)
                data.append({
                    "Swimmer": swimmer_name,
                    "Age": age,
                    "Distance": int(distance.replace('m','')),
                    "Stroke": stroke,
                    "Lap Times": lap_times,
                    "Total Time": total_time
                })
    return pd.DataFrame(data)

df = process_files()

def calculate_velocity(lap_times, distance):
    if not lap_times:
        return 0
    total_time = sum(lap_times)
    if total_time == 0:
        return 0
    return distance / (total_time / len(lap_times))

def generate_recommendation(swimmer_df):
    lap_time_variations = swimmer_df['Lap Times'].apply(lambda x: np.std(x))
    avg_variation = lap_time_variations.mean()

    if avg_variation > 5:
        return "Focus on maintaining a consistent pace throughout the race."
    else:
        return "Your pacing is relatively consistent. Keep up the good work!"

def analyze_swimmer(swimmer_name):
    swimmer_df = df[df["Swimmer"] == swimmer_name].copy()
    if swimmer_df.empty:
        return {"error": "Swimmer Not found"}

    swimmer_df['Average Lap Time'] = swimmer_df['Lap Times'].apply(lambda x: sum(x) / len(x))

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(swimmer_df.index, swimmer_df["Total Time"])
    plt.title(f"{swimmer_name} - Total Race Times")
    plt.xlabel("Race")
    plt.ylabel("Total Time (seconds)")

    plt.subplot(1, 2, 2)
    bar_width = 10
    for stroke in swimmer_df['Stroke'].unique():
        stroke_data = swimmer_df[swimmer_df['Stroke'] == stroke]
        plt.bar(stroke_data['Distance'], stroke_data['Average Lap Time'],
                label=stroke, width=bar_width)
    plt.title(f"{swimmer_name} - Average Lap Times by Distance and Stroke")
    plt.xlabel("Distance (m)")
    plt.ylabel("Average Lap Time (seconds)")
    plt.legend()

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    X = swimmer_df.index.values.reshape(-1, 1)
    y = swimmer_df["Total Time"].values

    model = LinearRegression()
    model.fit(X, y)

    next_race = np.array([[X[-1][0] + 1]])
    predicted_time = model.predict(next_race)[0]

    velocity = calculate_velocity(swimmer_df['Lap Times'].iloc[0], swimmer_df['Distance'].iloc[0])

    age = swimmer_df['Age'].iloc[0]
    distance = swimmer_df['Distance'].mean()
    mhr = 220 - age

    if distance <= 50:
        heart_rate = mhr * 0.85
    elif distance <= 100:
        heart_rate = mhr * 0.75
    else:
        heart_rate = mhr * 0.65

    age = swimmer_df['Age'].iloc[0]
    age = int(age)

    metrics = {
        "Total Time": "{:.2f}".format(swimmer_df["Total Time"].mean()),
        "Average Lap Time": "{:.2f}".format(swimmer_df["Average Lap Time"].mean()),
        "Velocity": "{:.2f}".format(velocity),
        "Distance": "{:.2f}".format(swimmer_df['Distance'].mean()),
        "Predicted Time": "{:.2f}".format(predicted_time),
        "Heart Rate": "{:.2f}".format(heart_rate),
    }

    metric_recommendations = []

    # Adjusted Thresholds
    if float(metrics["Average Lap Time"]) > 100:  # Adjusted threshold
        metric_recommendations.append("Your average lap time is higher than expected. Consider focusing on refining your stroke technique and building endurance.")

    if float(metrics["Velocity"]) < 1.2:  # Adjusted threshold
        metric_recommendations.append("Your velocity could be improved. Focus on increasing your stroke efficiency and power to swim faster.")

    if float(metrics["Heart Rate"]) < 110:  # Adjusted threshold
        metric_recommendations.append("Your heart rate during longer swims is consistently low. Consider increasing the intensity of your workouts.")
    elif float(metrics["Heart Rate"]) > 190:  # Adjusted threshold
        metric_recommendations.append("Your heart rate during longer swims is consistently high. Focus on pacing yourself more effectively to avoid overexertion.")

    if float(metrics["Predicted Time"]) > float(metrics["Total Time"]) * 1.05:  # Adjusted threshold
        metric_recommendations.append("Your predicted time shows a potential decrease in performance. Review your training strategy to identify areas for improvement.")
    elif float(metrics["Predicted Time"]) < float(metrics["Total Time"]) * 0.95:  # Adjusted threshold
        metric_recommendations.append("Your predicted time shows a potential improvement. Continue with your current training strategy to maximize your performance.")

    recommendation = generate_recommendation(swimmer_df)

    print(metric_recommendations)
    return {"plot": plot_url, "metrics": metrics, "recommendation": recommendation, "metric_recommendations": metric_recommendations, "age": age}

@app.route('/swimmer/<name>')
def get_swimmer_data(name):
    result = analyze_swimmer(name)
    return jsonify(result)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)