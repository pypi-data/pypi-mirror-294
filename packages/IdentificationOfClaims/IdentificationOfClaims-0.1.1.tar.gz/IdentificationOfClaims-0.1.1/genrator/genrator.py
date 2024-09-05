import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def genrate_response(prompt1):

    response = model.generate_content(prompt1)
    return response
    # try:    
    #     # print(response.text)
    # except Exception as error:
    #     print("Someting Got Wrong")
    #     print(error)
    #     return {"text":0,"error_message":"Someting Got Wrong"}
