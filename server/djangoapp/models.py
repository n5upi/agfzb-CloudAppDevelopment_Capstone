''' django models '''
from django.db import models
from django.core import serializers
import uuid
import json
#from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    ''' CarMake models '''
    name = models.CharField(null=False, max_length=30, default='')
    description = models.CharField(max_length=1000)
    def __str__(self):
        #return "Make: " + self.name + \
        #       "Description: " + self.description

        #return "Name: " + self.maker_name
        
        return "Name: " + self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model
#  (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited
#  choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    ''' CarModels '''
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    #dealer_id = models.IntegerField()
    #id = models.IntegerField(default=1,primary_key=True)
    dealer_id = models.IntegerField(default=1,primary_key=True)
    name = models.CharField(null=False, max_length=30, default='')
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    COUPE = 'Coupe'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe')
    ]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    year = models.DateField()
    def __str__(self):
        #return " Make Name: "+ self.make.name + \
        #       "Name: " + self.name + \
        #       " Type: " + self.type + \
        #       " Dealer ID: " + str(self.dealer_id)+ \
        #       " Year: " + str(self.year)

        #return "Name: " + self.model_name

        return "Name: " + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    ''' DealerReview '''
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment #Watson NLU service
        self.id=id

    def __str__(self):
        return "Review: " + self.review +\
                " Sentiment: " + self.sentiment
