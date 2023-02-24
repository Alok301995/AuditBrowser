from fastapi import FastAPI 
from src.routes import prediction
from src.model import Database
from src.routes import fetch_data

####################################################################################

app = FastAPI()

####################################################################################

db = Database('database.db')
db.create_table()

####################################################################################


app.include_router(prediction.router)
app.include_router(fetch_data.router)

####################################################################################
