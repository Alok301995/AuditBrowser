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

    def record_fingerprint(self, attributes, cookie, ip ,signature , signature_mobile, is_mobile):
        
        '''
        Function to record the fingerprint data
        
        '''
                
        # if self._need_to_record(cookie, signature, ip):
        self._record_attributes(attributes, signature , signature_mobile , is_mobile)
        #     pass
        
                
    ################################################################################


    def _record_attributes(self, attributes, signature , signature_mobile , is_mobile):
        '''
        Function to record the attributes of the fingerprint
        '''
        try:
            db.record_fingerprint(attributes , signature , signature_mobile)
            md5_attributes = FingerprintHelper().create_md5_values(attributes)
            # print(len(md5_attributes))
            if is_mobile == False:
                db.update_totals_table(md5_attributes, signature,is_mobile)
            else :
                db.update_totals_table(md5_attributes, signature_mobile,is_mobile)
                
        
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
    
   
# import re
# import numpy as np
# from sklearn.cluster import MiniBatchKMeans

# def cluster_user_agents(user_agents, k=5, batch_size=1000, max_iter=100):
#     """
#     Clusters user agents using streaming k-means.

#     Args:
#         user_agents (list): List of user agent strings.
#         k (int): Number of clusters.
#         batch_size (int): Batch size for mini-batch k-means.
#         max_iter (int): Maximum number of iterations for mini-batch k-means.

#     Returns:
#         dict: Dictionary mapping cluster centers (as strings) to lists of user agents in that cluster.
#     """

#     # Compile regular expression pattern for extracting features from user agents
#     pattern = r'\((.*?)\)'

#     # Define function for extracting features from user agent string
#     def extract_features(ua):
#         matches = re.findall(pattern, ua)
#         return np.array([len(matches), len(ua)])

#     # Initialize mini-batch k-means model
#     kmeans = MiniBatchKMeans(n_clusters=k, batch_size=batch_size, max_iter=max_iter)

#     # Initialize dictionary for mapping cluster centers to lists of user agents
#     clusters = {}

#     # Iterate over user agents and cluster them using streaming k-means
#     for ua in user_agents:
#         # Extract features from user agent string
#         x = extract_features(ua)

#         # Predict cluster for user agent
#         label = kmeans.partial_fit([x]).labels_[0]

#         # Add user agent to appropriate cluster
#         center_str = str(kmeans.cluster_centers_[label])
#         if center_str not in clusters:
#             clusters[center_str] = []
#         clusters[center_str].append(ua)

#     return clusters


#     from sklearn.cluster import MiniBatchKMeans
#     from collections import defaultdict

#     def cluster_user_agents(user_agents, num_clusters):
#         """
#         Clusters user agents using streaming k-means and returns the cluster size and total number of user agents.
        
#         Args:
#         user_agents (list): A list of user agent strings.
#         num_clusters (int): The number of clusters to use for k-means clustering.
        
#         Returns:
#         A tuple of the form (cluster_size, total_num_user_agents), where cluster_size is a list of the size of each cluster
#         and total_num_user_agents is the total number of user agents.
#         """
#         cluster_model = MiniBatchKMeans(n_clusters=num_clusters)
#         cluster_size = defaultdict(int)
#         total_num_user_agents = 0
        
#         for user_agent in user_agents:
#             cluster_model.partial_fit([user_agent])
#             label = cluster_model.predict([user_agent])[0]
#             cluster_size[label] += 1
#             total_num_user_agents += 1
        
#         return (list(cluster_size.values()), total_num_user_agents)
        
