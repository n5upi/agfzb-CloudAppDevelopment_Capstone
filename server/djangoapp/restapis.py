import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from django.http import JsonResponse

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        if api_key:
            # Use HTTP Basic Authentication with the provided API key
            response = requests.get(url, headers=headers, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # No authentication, standard GET request
            response = requests.get(url, headers=headers, params=kwargs)
    except Exception as err:
        # Handle exceptions here
        print("Network exception occurred:", str(err))
        return None
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    
    try:
        json_data = json.loads(response.text)
        return json_data
    except json.JSONDecodeError:
        return None

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



