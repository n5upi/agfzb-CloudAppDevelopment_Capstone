''' javascrip oject notation '''
import json
import requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from .models import CarDealer

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    ''' no exception type '''
    print("GET from {} ".format(url))
    headers = {'Content-Type': 'application/json'}
    try:
        if api_key:
            # Use HTTP Basic Authentication with the provided API key
            response = requests.get(url, headers=headers, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers=headers, params=kwargs)
    except Exception as err:
        # If any error occurs
        print("Network exception occurred:", str(err))
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
def get_dealers_from_cf(url, **kwargs):
    ''' is not defined '''
    print(kwargs)
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result["row"]
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(dealership):
    # Replace with your actual cloud function URL
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/5d99be26-df44-44cf-aef4-34de1d685bf2/dealership-package/get-review"
    response = requests.get(url, params={'dealership': dealership})
    api_key = "vNXgiJpAvTd7uftgBCeQOCsNBcdlEzRU6xlMHKYcqEu0"
    dealer_reviews = []
    if response.status_code == 200:
        data = response.json()
        reviews_data = data.get('reviews', [])
        for review_data in reviews_data:
            review = DealerReview(
                dealership=review_data.get("dealership", ""),
                name=review_data.get("name", ""),
                purchase=review_data.get("purchase", ""),
                review=review_data.get("review", ""),
                purchase_date=review_data.get("purchase_date", ""),
                car_make=review_data.get("car_make", ""),
                car_model=review_data.get("car_model", ""),
                car_year=review_data.get("car_year", ""),
                sentiment=review_data.get("sentiment", ""),  # You need to define analyze_review_sentiments function
                id=review_data.get("id", "")
            )
            # Analyze sentiment and assign it to the review object
            sentiment = analyze_review_sentiments(review.review, api_key)
            if sentiment:
                review.sentiment = sentiment
            dealer_reviews.append(review)

    return dealer_reviews

def get_dealer_by_id_from_cf(id):
    url = f"https://us-east.functions.appdomain.cloud/api/v1/web/befaae8a-3d64-42a4-9aab-bdbd5aa2dd89/dealership-package/get_specific_dealer?id={id}"
    # Call get_request with a URL parameter
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        dealers = data.get('dbs', [])  # Assuming 'dbs' contains the list of dealers
        
        # Check if there are dealers in the list
        if dealers:
            # Take the first dealer (assuming there's only one)
            dealer_details = dealers[0]
            print("Dealer details:", dealer_details)  # Add this line for debugging
            
            # Create a CarDealer object with values from the dealer_details dictionary
            dealer_obj = CarDealer(
                address=dealer_details.get("address", "N/A"),
                city=dealer_details.get("city", "N/A"),
                full_name=dealer_details.get("full_name", "N/A"),
                id=dealer_details.get("id", "N/A"),
                lat=dealer_details.get("lat", "N/A"),
                long=dealer_details.get("long", "N/A"),
                short_name=dealer_details.get("short_name", "N/A"),
                st=dealer_details.get("st", "N/A"),
                zip=dealer_details.get("zip", "N/A")
            )
            
            return dealer_obj  # Return the CarDealer object directly
  
    return None

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
