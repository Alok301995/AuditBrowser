from fastapi import FastAPI, Response, Request ,Query
from src.routes import prediction
from src.model import Database
from src.routes import fetchData
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
####################################################################################
app = FastAPI()
app.mount("/static", StaticFiles(directory="./src/static"), name="static")
templates = Jinja2Templates(directory="./src/templates")
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
    return templates.TemplateResponse("new_index.html", {"request": request})
    

################################################################################

app.include_router(prediction.router)
app.include_router(fetchData.router)