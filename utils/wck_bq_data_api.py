# # -*- coding: utf-8 -*-

# =============================================================================
# Modules - Libraries
# =============================================================================

import sys
import requests
import json
import pandas as pd
import numpy as np
import logging


requests.packages.urllib3.disable_warnings()

# =============================================================================
# Settign the path variabless
# =============================================================================
wck_url = r"https://active-recipients-1003375120536.us-central1.run.app/query?limit=10000"


##
#############################################################
# FUNCTIONS
#############################################################

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up a simple logger -
    https://engineeringfordatascience.com/posts/python_logging/"""
    
    log = logging.getLogger(__name__)
    console = logging.StreamHandler()
    log.addHandler(console)
    log.setLevel(level)
    return log


# the main function that collects records from WCK API to post to ArcGIS
def wck_data(res):
    """This function takes the server response and creates
    a pandas dataframe with the json response

    Args:
        res (str): json file

    Returns:
        pd.dataframe: pandas dataframe with the activation data
    """
    
    '''the data in the response is under the rows key'''
    json_res = json.loads(res.content)
    
    # Load response into a dataframe
    df = pd.DataFrame(json.loads(json_res['rows']))
        
    log.info(f"\n --- \n There are: {df.shape[0]} "
             "records in the API \n --- \n")
    
    return df


# def wck_api(cloud_function_token):
#     """This function checks the status of the response when 
#     using the activation data end point

#     Args:
#         cloud_function_token (str): WCK token 

#     Returns:
#         pd.dataframe: pandas dataframe with the activation data
#     """
    
#     # Make the POST request
#     response = requests.post(wck_url, 
#                              json={"auth_token": cloud_function_token})


#     # Check the response status code
#     if response.status_code == 200:
#         api_data = wck_data(response) # run the main script to manage data
#     else:
#         sys.exit()
    
#     return api_data


def wck_api(cloud_function_token):
    """This function checks the status of the response when 
    using the activation data end point

    Args:
        cloud_function_token (str): WCK token 

    Returns:
        pd.dataframe: pandas dataframe with the activation data
    """
    
    # # Make the POST request
    
    # Let `requests` set Content-Type for us by using `json=...`
    payload = {"auth_token": cloud_function_token}
    response = requests.post(wck_url, json=payload, timeout=20)

    # Check the response status code
    if response.status_code == 200:
        api_data = wck_data(response) # run the main script to manage data
    else:
        log.info(f"\n --- \n POST request failed with status code: "
                 f"{response.status_code}\n --- \n")
        log.info(f"\n --- \n {response.content}\n --- \n")
        sys.exit()
    
    return api_data
    
# Set log level to info
log = setup_logging()