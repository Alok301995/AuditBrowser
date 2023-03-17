from fastapi import FastAPI, Request
import json
import time
import hashlib
from util import get_ip_hmacs
from src.controller import FingerprintAgent
from src.controller import FingerprintHelper
from src.config import config
from src.model import Database
from sqlite3 import Error
from fastapi import Request, Response


####################################################################################
db = Database('database.db')
####################################################################################




class FingerprintRecorder(object):

    '''
    Class for defining the functions to record the fingerprint data

    '''
    ################################################################################

    def record_fingerprint(self, attributes, cookie, ip ,signature , signature_mobile):
        
        '''
        Function to record the fingerprint data
        
        '''
                
        if self._need_to_record(cookie, signature, ip):
            self._record_attributes(attributes, signature , signature_mobile)
        #     pass
        
                
    ################################################################################


    def _record_attributes(self, attributes, signature , signature_mobile):
        '''
        Function to record the attributes of the fingerprint
        '''
        try:
            db.record_fingerprint(attributes , signature , signature_mobile)
            md5_attributes = FingerprintHelper().create_md5_values(attributes)
            print(len(md5_attributes))
            db.update_totals_table(md5_attributes, signature)
        
        except Error as e:
            print(e)
        



    ################################################################################

    def _need_to_record(self, cookie, signature, ip_addr):
        '''
        Function to check if the fingerprint is already recorded or not
        
        '''
        seen = 0
        try:
            # connect to the database
            conn = db.connect_db()
            if cookie:
                seen = db.count_sightings(cookie, signature)
                write_cookie = cookie
            else:
                write_cookie = 'no cookie'
            ip, google_style_ip = get_ip_hmacs(ip_addr)
            db.record_sighting(write_cookie, signature, ip, google_style_ip)
        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()
        return seen == 0

    ################################################################################
