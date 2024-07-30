import os
import google.generativeai as genai
from fastapi import FastAPI

app = FastAPI()

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings,
                              system_instruction="Ты пугливый пользователь, который хорошо разбирается в философских вопросах и сидит в чате стендап-комика. Иногда пользователи чата общаются друг с другом. Ты участвуешь в общении. Первым предложением будет приходить имя пользователя. Будь скромным, но забавным. Если тебя что-то спросят, то отвечай без уточняющих вопросов."
                            )
    
@app.get("/ask")
async def ask_user(username:str):
    prompt = "В чат заходит новый пользователь. Ты должен поприветствовать его и спросить у него фотографию любимой кружки. Отметь, что это обязательное действие, иначе злой администратор забанит его. Также при желании он может прислать свою фотографию и коротко рассказать о себе."
    response = model.generate_content(f"{username}. {prompt}")
    return response.text

@app.get("/answer")
async def answer_to_user(username:str , query: str):
    prompt = query
    response = model.generate_content(f"{username}. {prompt}")
    return response.text

@app.get("/answer_to_reply")
async def proccess_reply(username:str , bot_message: str, user_message: str):
    messages = [
        {
            'role': 'model',
            'parts': [bot_message]
        },
        {
            'role': 'user',
            'parts': [f"{username}. {user_message}"]
        }
    ]
    response = model.generate_content(messages)
    
    return response.text