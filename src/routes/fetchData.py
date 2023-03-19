from fastapi import APIRouter, Request, Response , Query
from src.controller import FingerprintAgent, FingerprintHelper, FingerprintRecorder, Entropy
from src.services import detect_activity, create_df, convert_data
import hashlib
import json
from src.model import Database

################################################################################
router = APIRouter()
################################################################################

# Router for fetching data from the client
# Seperate the accelerometer data and gyroscope data from the recived data
# and send it to the to another route for processing.

################################################################################

@router.post("/api/fetch_data")
async def fetch_data(request: Request , response : Response):
    try:
        req = await request.body()
        # print(req)
        data = req.decode('utf8').replace("'", '"')
        # print(data)
        data = json.loads(data)
        # print(data)
        # print("data recived from the server" , data)
        
        # print(data)
        val =  False
        if data:
            # get the server side attributes
            agent = FingerprintAgent(request)
            server_attribues = agent.detect_server_attributes()
            # print(server_attribues)
            # Step to verify the incomming data
            attributes = server_attribues.copy()

            activity = "N/A"  
            data_points = []
            accelerometer_data = data["accelerometer"]
            if accelerometer_data:
                data_points = convert_data(accelerometer_data)
                df = create_df(data_points)
                activity = detect_activity(df)

            # fill the valid_attributes with the data from the client
            for key in data:
                attributes[key] = str(data[key])

            attributes["activity"] = activity


            # print(attributes)
            # pass the complete attributes to the next route using middleware

            recorder = FingerprintRecorder()
            entropy = Entropy()

            cookie = request.cookies.get('long_cookie') or {}
            ip_addr = request.client.host.split(":")[0]
            
            # Validate the attributes
            valid_attributes, signature, signature_mobile = verify_attributes(attributes)
            print(valid_attributes)
            recorder.record_fingerprint(valid_attributes, cookie, ip_addr,signature , signature_mobile)
           
            res = entropy.get_bits_of_info(valid_attributes, signature , signature_mobile)
            
            return {"status": True ,"data":res}
        else:
            return {"status": False , "data":"Not able to fetch data from the client"}

    except Exception as e:
        print(e)
        return {"status" : False , "data":e}


################################################################################

def verify_attributes(attributes):
    '''
    Function to verify the attributes
    
    '''
    helper = FingerprintHelper()

    # Get the list of valid attributes from the fingerprint helper
    valid_attributes_list = list(helper.attributes.keys())
    
    # append the signature to the valid attributes
    valid_attributes_list.append('signature')

    
    desk_attributes = attributes.copy()
    desk_attributes['activity'] = 'N/A'
    
    # Signature for mobile
    sorter_valid_attributes = sorted(attributes.items())
    serialized_attributes = json.dumps(sorter_valid_attributes)
    signature_mobile = hashlib.md5(serialized_attributes.encode(
        'ascii', 'ignore')).hexdigest()
    

    # Signature for desktop
    sorted_desktop_attributes =  sorted(desk_attributes.items())
    serialized_attributes_desktop = json.dumps(sorted_desktop_attributes)
    signature = hashlib.md5(serialized_attributes_desktop.encode(
        'ascii', 'ignore')).hexdigest()
    
    attributes['signature'] = signature
    
    valid_attributes = {}

    for i in attributes:
        if i in valid_attributes_list:
            valid_attributes[i] = attributes[i]
    
    return  valid_attributes, signature, signature_mobile

################################################################################
