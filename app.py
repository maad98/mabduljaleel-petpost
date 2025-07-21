from flask import Flask, render_template, request, redirect
import boto3
import os
import json
from datetime import datetime

app = Flask(__name__)

S3_BUCKET = 'petpost-images-mabduljaleel'  # 🔁 Replace with your real bucket name
JSON_FILE = 'pets.json'

s3 = boto3.client('s3')

# Load pet list
def load_pets():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, 'r') as f:
        return json.load(f)

# Save pet list
def save_pets(pets):
    with open(JSON_FILE, 'w') as f:
        json.dump(pets, f)

@app.route('/')
def index():
    pets = load_pets()
    return render_template('index.html', pets=pets)

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    age = request.form['age']
    breed = request.form['breed']
    image = request.files['image']

    if image:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        image_filename = f"{timestamp}_{image.filename}"
        s3.upload_fileobj(image, S3_BUCKET, image_filename)
        image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{image_filename}"

        pets = load_pets()
        pets.append({
            'name': name,
            'age': age,
            'breed': breed,
            'image_url': image_url
        })
        save_pets(pets)

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

