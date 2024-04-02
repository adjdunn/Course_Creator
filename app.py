from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import os
from openai import OpenAI
import random
import json

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/create-outline', methods=['POST'])
def create_outline():
    course_subject = request.form['course-subject']
    course_description = request.form['course-description']

    prompt = open('course_outline_prompt.txt', 'r').read() % (course_subject, course_description)

    response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
            {
                "role": "user",
                "content": prompt
            }
            ],
            temperature=1,
            max_tokens=2772,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )


    dataRaw = response.choices[0].message.content

    data = dataRaw.replace("```json", "").replace("```", "")

    data_num = random.randint(100, 10000)
    
    fileName = f'data_{data_num}.json'
    filePath = os.path.join(app.root_path, 'static', 'data', fileName)
    
    with open(filePath, 'w') as f:
        json.dump(eval(data), f, indent=4)

    return redirect(f'/view-outline/{data_num}')


@app.route('/view-outline/<int:data_num>')
def view_outline(data_num):

    # fileName = f'data_{data_num}.json'
    # filePath = os.path.join(app.root_path, 'static', 'data', fileName)
    
    # with open(filePath, 'r') as f:
    #     data = json.load(f)

    # return data

    return render_template('index.html', data_num=data_num)
    


if __name__ == '__main__':
    app.run(debug=True)