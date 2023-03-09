from fastapi import FastAPI, Response, Request
from src.routes import prediction
from src.model import Database
from src.routes import fetchData
from fastapi.middleware.cors import CORSMiddleware

####################################################################################

app = FastAPI()

####################################################################################

db = Database('database.db')
db.create_table()

####################################################################################

app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)




@app.get('/')
async def index(request: Request, response: Response):

    if 'long_cookie' in request.cookies:
        print(request.cookies['long_cookie'])
    else:
        response.set_cookie(key='long_cookie', value='some value',
                            max_age=31536000, httponly=True)

    return {"message": "This is Home page"}

app.include_router(prediction.router)
app.include_router(fetchData.router)


####################################################################################
