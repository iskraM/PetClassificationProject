from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from pymongo import MongoClient
from datetime import datetime
#import openai
from bs4 import BeautifulSoup

#python -m flask --debug run

#region CONFIG
client = MongoClient('mongodb+srv://test123:test123@cluster0.zy8ouhh.mongodb.net/?retryWrites=true&w=majority')
db = client.IISprojekt
zivali = db.zivali

API_URL = "https://api-inference.huggingface.co/models/devMinty/iis-pet-classifier"
headers = {"Authorization": "Bearer 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"}
#openai.api_key = "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"

#endregion

app = Flask(__name__)
CORS(app)


# def generate_anwser(question):
#     responce = openai.Completion.create(
#         engine = "text-ada-001",
#         prompt = question,
#         max_tokens = 1024,
#         temperature = 0.7,
#         n=1,
#         stop = None,
#         timeout = 10,
#     )
#     anwser = responce.choices[0].text.strip()
#     return anwser



@app.route('/')
def starting():
    return "Hello world of inteligent systems"

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No image found", 400
    
    image = request.files['image']
    image_bytes = image.read()

    response = requests.post(API_URL, headers=headers, data=image_bytes)
    return response.json()

@app.route('/feedback', methods=['POST'])
def add_feedback():
    image = request.files['image'].read()
    predicted_label = request.form['predicted_label']
    true_label = request.form['true_label']
    description = request.form['description']
    time = datetime.now()
 
    if not image or not predicted_label or not description: 
        return "Missing data", 400

    zivali.insert_one({
        'image': image,
        'predicted_label': predicted_label,
        'true_label': true_label if true_label else predicted_label,
        'description': description,
        'time': time
    })

    return "Thank you!", 201

# @app.route('/aitest', methods=['POST'])
# def aitest():
#     question = request.form['question']
#     anwser = generate_anwser(question)
#     return jsonify({'anwser': anwser})


@app.route('/wikitest/<animal>', methods=['POST'])
def wikitest(animal):
    url = "https://en.wikipedia.org/wiki/" + animal
    if requests.get(url).status_code != 200:
        return jsonify({'paragraph': "No information found for used search parameter"})
    else:
        response = requests.get("https://en.wikipedia.org/wiki/" + animal)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')

        for paragraph in paragraphs:
            if animal in paragraph.get_text():
                paragraph_text = paragraph.get_text()
                paragraph_text = paragraph_text.replace('\n', '')
                paragraph_text = paragraph_text.replace('[1]', '')
                paragraph_text = paragraph_text.replace('[2]', '')
                paragraph_text = paragraph_text.replace('[3]', '')
                paragraph_text = paragraph_text.replace('[4]', '')
                paragraph_text = paragraph_text.replace('[5]', '')
                paragraph_text = paragraph_text.replace('[6]', '')
                break
            elif "_" in animal:
                wordeOne = animal.split("_")[0]
                if wordeOne in paragraph.get_text():
                    paragraph_text = paragraph.get_text()
                    paragraph_text = paragraph_text.replace('\n', '')
                    paragraph_text = paragraph_text.replace('[1]', '')
                    paragraph_text = paragraph_text.replace('[2]', '')
                    paragraph_text = paragraph_text.replace('[3]', '')
                    paragraph_text = paragraph_text.replace('[4]', '')
                    paragraph_text = paragraph_text.replace('[5]', '')
                    paragraph_text = paragraph_text.replace('[6]', '')
                    break
            elif " " in animal:
                wordeOne = animal.split(" ")[0]
                if wordeOne in paragraph.get_text():
                    paragraph_text = paragraph.get_text()
                    paragraph_text = paragraph_text.replace('\n', '')
                    paragraph_text = paragraph_text.replace('[1]', '')
                    paragraph_text = paragraph_text.replace('[2]', '')
                    paragraph_text = paragraph_text.replace('[3]', '')
                    paragraph_text = paragraph_text.replace('[4]', '')
                    paragraph_text = paragraph_text.replace('[5]', '')
                    paragraph_text = paragraph_text.replace('[6]', '')
                    break
            else:
                paragraph_text = "No information found"
        
        return jsonify({'paragraph': paragraph_text})



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
