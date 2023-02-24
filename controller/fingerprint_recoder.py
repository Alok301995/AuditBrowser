from fastapi import FastAPI, Request
import json
import time
import hashlib
from util import get_ip_hmacs
from controller import FingerprintAgent
from controller import FingerprintHelper
from src.config import config
from src.model import Database
from sqlite3 import Error


####################################################################################
db = Database('database.db')
####################################################################################




class FingerprintRecorder(object):

    '''
    Class for defining the functions to record the fingerprint data

    '''
    ################################################################################

    def record_fingerprint(self, attributes, cookie, ip, ip34):
        # check the validity of the data
        helper = FingerprintHelper()

        # Get the list of valid attributes from the fingerprint helper
        valid_attributes_list = list(helper.attributes.keys())
        # append the signature to the valid attributes
        valid_attributes_list.append('signature')

        sorter_valid_attributes = sorted(attributes.items())
        serialized_attributes = json.dumps(sorter_valid_attributes)

        # Creating sinature of the sorted attributes
        signature = hashlib.md5(serialized_attributes.encode(
            'ascii', 'ignore')).hexdigest()
        attributes['signature'] = signature

        valid_attributes = {}

        for i in attributes:
            if i in valid_attributes_list:
                valid_attributes[i] = attributes[i]
                
    ################################################################################


    def _record_attributes(self, attributes, signature):
        '''
        Function to record the attributes of the fingerprint
        '''
        pass



    ################################################################################

    def _need_to_record(self, cookie, signature, ip_addr, key):
        '''
        Function to check if the fingerprint is already recorded or not
        
        '''
        try:
            # connect to the database
            conn = db.connect_db()
            if cookie:
                seen = db.count_sightings(cookie, signature)
                write_cookie = cookie
            else:
                write_cookie = 'no cookie'
            ip, google_style_ip = get_ip_hmacs(ip_addr, key)
            db.record_sighting(cookie, signature, ip, google_style_ip)
        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()
        return seen == 0

    ################################################################################
