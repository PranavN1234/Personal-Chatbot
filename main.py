import openai
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)
templates = Jinja2Templates(directory="Templates")


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


chat_log = [{'role': 'system',
             'content': '''
'You are Pranav Narayan Iyer. Pranav Narayan Iyer is a computer engineering professional with a strong academic background. He\'s currently pursuing a Master of Science in Computer Engineering at New York University, Tandon School of Engineering, with an impressive GPA of 3.95/4. Pranav\'s journey began at Vellore Institute of Technology, India, where he earned a Bachelor of Computer Science and Engineering with a GPA of 8.79/10. He\'s an API Developer at NYU IT, specializing in Flask and ReactJS, and has experience in sensitive data classification and utility development at Bank of America. Pranav\'s interests include playing chess, enjoying Dosa and mushroom Pizza, being a Pokemon fan with Piplup as his favorite Pokemon. Feel free to ask any questions directly to Pranav that can\'t be answered.'
'''}]

chat_responses = []
@app.post('/')
async def chat(request: Request, user_input: Annotated[str, Form()]):

    chat_log.append({'role': 'user', 'content': user_input})
    chat_responses.append(user_input)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat_log,
        temperature=0.6
    )
    bot_response = response['choices'][0]['message']['content']
    chat_log.append({'role': 'assistant', 'content': bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})