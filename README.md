

# Flights-app
[![Build Status](https://travis-ci.org/dkam26/Flights-app.svg?branch=master)](https://travis-ci.org/dkam26/Flights-app)
[![Coverage Status](https://coveralls.io/repos/github/dkam26/Flights-app/badge.svg?branch=master)](https://coveralls.io/github/dkam26/Flights-app?branch=master)

=======
# Flights
Flights is an app helps users book flights to specific destinations.Users can view and book available flights after signing up the app.

## About
A user can book several flights

A user can delete their profile picture

A user can update their profile picture

A user can view their booked flights

A user can view all available flights

A user is required to include an e-mail address, name, first name,profile picture(.jpg and .png images ONLY) and password on creating an account



## Tools
Tools used for development of this API are;
- API development environment: [Postman](https://www.getpostman.com)
- Editor: [Vs code](https://code.visualstudio.com)
- Documentation : [Apiary](https://apiary.io/)
- Database: [Postgresql](https://www.postgresql.org)
- Framework: [Django](https://www.django-rest-framework.org/)
- Programming language: [Python 3.x.x](https://docs.python.org/3/)

## Tests

The tests are to confirm the connection to the database,accounts creation,login session,booking of flights.

To run the tests,use:

coverage run --source=flight_app manage.py test


## Getting Started

## URL of the API

https://flight-app-output.herokuapp.com/

## End points
### Endpoints to create a user account and login into the application
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /auth/register/ | True | Create an account
POST | /auth/login/ | True | Login a user
PUT  |  /auth/register/ | False | Change proflie image
DELETE  |  /auth/register/ | False | Delete proflie image


### Endpoints to create, update, view and delete a shopping list
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /flights/ | False | View all flights
POST | /book/flight/ | False | Book a flight
GET | /user/flights/ | False | View details of a shopping list





## Contributors

https//github.com/dkam26



