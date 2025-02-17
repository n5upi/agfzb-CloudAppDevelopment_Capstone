''' django imports '''
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer, CarModel, CarMake, DealerReview
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_request, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    ''' return about '''
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    ''' return contact '''
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
        
# Create a `login_request` view to handle sign in request
def login_request(request):
    ''' login page '''
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    ''' logout page '''
    # Get the user object based on request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    ''' registration page '''
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to index page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    ''' dealerships '''
    if request.method == "GET":
        context = {}
        # url is returning errors
        #url = "https://us-south.functions.appdomain.cloud/api/v1/web/e2297f16-3884-47c0-862c-4bc7dda3221d/dealership-package/get-dealership"
        # newly copied endpoint URL get-dealership.js inside function
        url = "https://dhuggins-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context["dealership_list"] = dealerships
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    ''' dealer details '''
    if request.method == "GET":
        context = {}
        # id == dealer_id
        # Call the get_dealer_reviews_from_cf function to get reviews
        reviews = get_dealer_reviews_from_cf(dealer_id)
        context["reviews"] = reviews
        print("Review object:", reviews)
        dealer = get_dealer_by_id_from_cf(dealer_id)
        print("Dealer object:", dealer)
        context["dealer"] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    ''' add review '''
    if request.method == "GET":
        # Use the get_dealer_by_id_from_cf function to fetch dealer details
        dealer = get_dealer_by_id_from_cf(dealer_id)
        context = {
            "cars": CarModel.objects.all(),
            "dealer": dealer,
            "dealer_id": dealer_id,
            "user": request.user  # Pass the user object
        }
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        # Check if the user is authenticated (logged in)
        if request.user.is_authenticated:
            # Handle the review submission here
            form = request.POST
            purchasecheck = "true" if "purchasecheck" in form else "false"
            review = {
                "name": f"{request.user.first_name} {request.user.last_name}",
                "dealership": dealer_id,
                "review": form["content"],
                "purchase": form.get("purchasecheck"),
            }
            
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").strftime("%m/%d/%Y")
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year.strftime("%Y")
            
            json_payload = {"review": review}
            URL = 'https://us-south.functions.appdomain.cloud/api/v1/web/c3b88ad1-688e-45eb-9475-3a3b1ffba86c/dealership-package/post-review'
            post_request(URL, json_payload)
            
            # Redirect to the dealer details page after review submission
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            # Redirect unauthenticated user to the index page
            return redirect("djangoapp:index")
