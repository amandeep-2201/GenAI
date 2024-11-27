#1. Library imports
import uvicorn
from fastapi import FastAPI

#2. Create the app object
app = FastAPI()

#3. Index route, opens automatically on http:/127:0:0.1:8000
@app.get("/")
def index():
    return{'message':'Hello, stranger'}

#4. Route with a single parameter, returns the parametere withi
#   Located at: https://127.0.0.1:8000/AnyNameHere

@app.get('/Welcome')
def get_name(name: str):
    return {'Welcome to Aman Coaching Classes': f'{name}'}

#5 Run the API with uvicorn
#   Will run on http://127.0.0.1:8000
if __name__ == "__main__":
    uvicorn.run(app, host = '127.0.0.1', port=8000)
    
#uvicorn main:app --reload

