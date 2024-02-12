import textwrap
from flask import Flask, request, jsonify
import google.generativeai as genai
from IPython.display import Markdown

from flask_cors import CORS  # Import the CORS extension

app = Flask(__name__)
CORS(app) 

genai.configure(api_key='AIzaSyCogaAiP16nUzFzyeUKXDGv5B0hEAg2xuo')  # Replace 'YOUR_API_KEY' with your actual API key

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
    app.run(port=5000)  # Run the Flask app on port 5000 or any other port you prefer


