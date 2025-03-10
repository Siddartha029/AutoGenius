from flask import Flask, request, jsonify, render_template
import os
import pandas as pd
import google.generativeai as genai

app = Flask(__name__)


genai.configure(api_key="AIzaSyATLmKLm2SdBOZF3RAtvZM2TG1sgDaFkr8")
# Load the CSV dataset
csv_file_path = os.path.join("data", "cars_ds_final.csv")
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"Error: CSV file not found at {csv_file_path}")
    df = None

# Initialize Gemini model (Gemini Flash)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route('/')
def index():
    return render_template('index.html', data={})

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/compare', methods=['GET'])
def compare_vehicles():
    vehicle1 = request.args.get('vehicle1')
    vehicle2 = request.args.get('vehicle2')

    if df is None:
        return jsonify({"error": "Dataset not loaded."}), 500

    if not vehicle1 or not vehicle2:
        return jsonify({"error": "Both vehicle1 and vehicle2 are required."}), 400

    try:
        vehicle1_lower = vehicle1.lower()
        vehicle2_lower = vehicle2.lower()

        vehicle1_row = df[df['Model'].str.lower().str.contains(vehicle1_lower)].iloc[0]
        vehicle2_row = df[df['Model'].str.lower().str.contains(vehicle2_lower)].iloc[0]

        specs1 = {
            "Ex-Showroom_Price": vehicle1_row.get("Ex-Showroom_Price", "N/A"),
            "Displacement": vehicle1_row.get("Displacement", "N/A"),
            "Fuel_Type": vehicle1_row.get("Fuel_Type", "N/A"),
            "Body_Type": vehicle1_row.get("Body_Type", "N/A"),
            "ARAI_Certified_Mileage": vehicle1_row.get("ARAI_Certified_Mileage", "N/A"),
            "Power": vehicle1_row.get("Power", "N/A"),
            "Torque": vehicle1_row.get("Torque", "N/A"),
            "Seating_Capacity": vehicle1_row.get("Seating_Capacity", "N/A"),
            "Fuel_Tank_Capacity": vehicle1_row.get("Fuel_Tank_Capacity", "N/A"),
        }

        specs2 = {
            "Ex-Showroom_Price": vehicle2_row.get("Ex-Showroom_Price", "N/A"),
            "Displacement": vehicle2_row.get("Displacement", "N/A"),
            "Fuel_Type": vehicle2_row.get("Fuel_Type", "N/A"),
            "Body_Type": vehicle2_row.get("Body_Type", "N/A"),
            "ARAI_Certified_Mileage": vehicle2_row.get("ARAI_Certified_Mileage", "N/A"),
            "Power": vehicle2_row.get("Power", "N/A"),
            "Torque": vehicle2_row.get("Torque", "N/A"),
            "Seating_Capacity": vehicle2_row.get("Seating_Capacity", "N/A"),
            "Fuel_Tank_Capacity": vehicle2_row.get("Fuel_Tank_Capacity", "N/A"),
        }

        # Gemini Integration: Generate a comparative summary
        prompt = f"Compare the following cars:\n\nCar 1: {vehicle1_row['Model']} - {specs1}\n\nCar 2: {vehicle2_row['Model']} - {specs2}\n\nProvide a brief summary of the key differences and similarities."
        response = model.generate_content(prompt)
        summary = response.text

        return jsonify({"specs1": specs1, "specs2": specs2, "summary": summary})

    except (KeyError, IndexError):
        return jsonify({"error": "Vehicle data not found"}), 404
    except Exception as e: # Catch other potential errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
