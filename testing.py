import json
from openai import OpenAI
import random

client = OpenAI()

def load_json():
    with open('data_2233.json', 'r') as f:
        return json.load(f)
    

def create_course_outline(course_description):
    
    prompt = open('course_outline_prompt.txt', 'r').read() % (course_description)

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
    
    return data


def save_json(data):
    
    data_num = random.randint(100, 10000)
    
    fileName = f'data_{data_num}.json'
    
    with open(fileName, 'w') as f:
        json.dump(eval(data), f, indent=4)
        
    return data_num
        



def create_course(course_description):
    data = create_course_outline(course_description)
    save_json(data)
    
    return 'Course Created'
    
    