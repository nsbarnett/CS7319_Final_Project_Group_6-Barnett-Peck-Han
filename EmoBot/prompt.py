from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key='sk-YzJPkL5VfeeQodVMqdNYYfXGAsAWn6ilEPy4Mua94QT3BlbkFJq6Y_EGq5n397wxXzBkc20WBy1u_ZRdSnEGl0Ge-Z4A')

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
def chat(input: ChatInput):
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::BLXyxoHx",
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input.message}
        ]
    )
    return {"response": completion.choices[0].message.content}

# Run the FastAPI Server in terminal...
# navigate to directory in terminal and then execute the following command
# uvicorn prompt:app --reload

# server is live at http://127.0.0.1:8000
# Send a post request to 
# http:// 127.0.0.1:8000/chat
# With json body including the chat like this
'''
{
  "message": "Can you help me calm down from an anxiety attack?"
}
'''

# You can also test out a post request with this UI given by FastAPI
# http://127.0.0.1:8000/docs

# To make this accessible through the web, not just locally, install ngrok
# After FastAPI server is running, run 
# ngrok http 8000
# This will give a URL for others to access my FastAPI server hosted on my machine