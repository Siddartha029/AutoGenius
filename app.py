from flask import Flask, request, jsonify, render_template
import os
import pandas as pd

app = Flask(__name__)

# Load the CSV dataset
csv_file_path = os.path.join("data", "cars_ds_final.csv")  # Replace with your filename
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"Error: CSV file not found at {csv_file_path}")
    df = None

@app.route('/')
def index():
    return render_template('index.html', data={}) #Pass empty data

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/compare', methods=['GET'])
def compare_vehicles():
    vehicle1 = request.args.get('vehicle1')
    vehicle2 = request.args.get('vehicle2')

    if df is None:
        return jsonify({"error": "Dataset not loaded."}), 500

    try:
        # Find vehicle data in the DataFrame (adjust 'Model' to match your data)
        vehicle1_row = df[df['Model'] == vehicle1].iloc[0]
        vehicle2_row = df[df['Model'] == vehicle2].iloc[0]

        # Extract specifications (adjust column names)
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

        return jsonify({"specs1": specs1, "specs2": specs2})

    except (KeyError, IndexError):
        return jsonify({"error": "Vehicle data not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)