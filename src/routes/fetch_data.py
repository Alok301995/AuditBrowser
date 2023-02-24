from fastapi import APIRouter, Request
from controller import FingerprintAgent, FingerprintHelper , FingerprintRecorder
from src.services import detect_activity, create_df, convert_data

################################################################################
router = APIRouter()
################################################################################

# Router for fetching data from the client
# Seperate the accelerometer data and gyroscope data from the recived data
# and send it to the to another route for processing
################################################################################
@router.post("/api/fetch_data")
async def fetch_data(request: Request):

    body = await request.json()

    data = body["attributes"]

    # get the server side attributes
    agent = FingerprintAgent(request)
    server_attribues = agent.detect_server_attributes()

    # Step to verify the incomming data
    attributes = server_attribues.copy()

    # Steps ahead
    # get the accelerometer data from valid_attributes
    # process it and attach the activity to activity variable
    # get the activity of the user from the accelerometer data

    activity = "None"
    if data:
        data_points = []
        accelerometer_data = data["accelerometer"]['data']
        if accelerometer_data:
            data_points = convert_data(accelerometer_data)
            df = create_df(data_points)
            activity = detect_activity(df)

    # fill the valid_attributes with the data from the client
    for key in data:
        attributes[key] = str(data[key])

    attributes["activity"] = activity
    
    
    # pass the complete attributes to the next route using middleware
    
    recorder = FingerprintRecorder()
    
    recorder.record_fingerprint(attributes)

    

    return {"status": "success"}
    # return {"status" : "success"}

################################################################################