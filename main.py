from fastapi import FastAPI, Response, Request ,Query
from src.routes import prediction
from src.model import Database
from src.routes import fetchData
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# fastapi cors
from fastapi.middleware.cors import CORSMiddleware

####################################################################################
app = FastAPI()
app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
####################################################################################

db = Database('database.db')
db.create_table()


####################################################################################
@app.get('/')
async def index(request: Request, response: Response , data: str = Query(None)):

    if 'long_cookie' in request.cookies:
        print(request.cookies['long_cookie'])
    else:
        response.set_cookie(key='long_cookie', value='some value',
                            max_age=31536000, httponly=True)

    # return {"message": "This is Home page"}
    return templates.TemplateResponse("index.html", {"request": request})
    

################################################################################

app.include_router(prediction.router)
app.include_router(fetchData.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)