import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
import numpy as np
import base64
from io import BytesIO
import textwrap
import google.generativeai as genai



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
genai.configure(api_key='AIzaSyCogaAiP16nUzFzyeUKXDGv5B0hEAg2xuo')  # Replace 'YOUR_API_KEY' with your actual API key

@app.route('/predict', methods=['POST'])
def predict():
    try:
        symptoms = request.json.get('symptoms')
        data = pd.read_csv("CSV_files/training_data.csv")
        test_data = pd.read_csv("CSV_files/test_data.csv")
        input_list=np.zeros(133)
        column_list = test_data.columns
        for i in range(len(column_list)):
            if column_list[i] in symptoms:
                input_list[i] = 1
        input_list= (np.array(input_list))

        model = RandomForestClassifier(n_estimators=100, random_state=42)  # Example model initialization

        X = data.drop(columns=["prognosis"])
        y = data["prognosis"]

        imputer = SimpleImputer(strategy='most_frequent')
        X_imputed = imputer.fit_transform(X)

        model.fit(X_imputed, y)

        input_symptom = input_list # Convert the input symptom value into the appropriate format
        input_symptom_imputed = imputer.transform([input_symptom])  # Handle missing values if any
        predicted_probabilities = model.predict_proba(input_symptom_imputed)

        top_5_indices = predicted_probabilities.argsort()[0][-5:][::-1]
        top_5_diseases = model.classes_[top_5_indices]
        top_5_probabilities = predicted_probabilities[0][top_5_indices]

        print("Top 5 diseases with highest probabilities:")
        for disease, probability in zip(top_5_diseases, top_5_probabilities):
            print(f"Disease: {disease}, Probability: {probability:.4f}")

        plt.figure(figsize=(10, 6))
        plt.barh(top_5_diseases, top_5_probabilities, color='skyblue')
        plt.xlabel('Probability')
        plt.ylabel('Disease')
        plt.title('Top 5 Diseases with Highest Probabilities')
        plt.gca().invert_yaxis()  # Invert y-axis to display highest probability at the top

        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png')
        image_data = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
        
        result = {
            "top_diseases": list(top_5_diseases),
            "probabilities": list(top_5_probabilities),
            "image_data": image_data
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.get_json()
    prompt = data.get('prompt', '')
    print(prompt)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    print(response.text)
    
    markdown_text = response.text.replace('•', '  *')
    indented_markdown = textwrap.indent(markdown_text, '> ', predicate=lambda _: True)
    
    return jsonify({'generated_content': indented_markdown})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)