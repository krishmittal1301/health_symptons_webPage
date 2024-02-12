import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get symptoms from the JSON request
        symptoms = request.json.get('symptoms')
        # print(symptoms)
        # Load the dataset
        data = pd.read_csv("training_data.csv")
        test_data = pd.read_csv("test_data.csv")
        input_list=np.zeros(133)
        column_list = test_data.columns
        for i in range(len(column_list)):
            if column_list[i] in symptoms:
                input_list[i] = 1
        input_list= (np.array(input_list))

        # Load the trained model
        model = RandomForestClassifier(n_estimators=100, random_state=42)  # Example model initialization

        # Assuming 'X' contains the symptoms/features and 'y' contains the target variable (diseases)
        X = data.drop(columns=["prognosis"])
        y = data["prognosis"]

        # Handle missing values if any
        imputer = SimpleImputer(strategy='most_frequent')
        X_imputed = imputer.fit_transform(X)

        # Train the model
        model.fit(X_imputed, y)

        # Convert the input symptom value into the appropriate format (e.g., convert to numpy array)
        input_symptom = input_list # Convert the input symptom value into the appropriate format

        # Make predictions for the input symptom
        input_symptom_imputed = imputer.transform([input_symptom])  # Handle missing values if any
        predicted_probabilities = model.predict_proba(input_symptom_imputed)

        # Get the top 5 diseases with highest probabilities
        top_5_indices = predicted_probabilities.argsort()[0][-5:][::-1]
        top_5_diseases = model.classes_[top_5_indices]
        top_5_probabilities = predicted_probabilities[0][top_5_indices]

        # Display the results
        print("Top 5 diseases with highest probabilities:")
        for disease, probability in zip(top_5_diseases, top_5_probabilities):
            print(f"Disease: {disease}, Probability: {probability:.4f}")

        plt.figure(figsize=(10, 6))
        plt.barh(top_5_diseases, top_5_probabilities, color='skyblue')
        plt.xlabel('Probability')
        plt.ylabel('Disease')
        plt.title('Top 5 Diseases with Highest Probabilities')
        plt.gca().invert_yaxis()  # Invert y-axis to display highest probability at the top
        plt.savefig("chart.png")
        plt.show()

        
        result = {
            "top_diseases": list(top_5_diseases),
            "probabilities": list(top_5_probabilities)
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=5000)