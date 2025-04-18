## How to use environment variables in get files

$ touch .env
Add the api keys like

# Accuweather (weather)
ACCUWEATHER_API_KEY=<key>

# Amedus (flights)
AMEDUS_BEARER_TOKEN=<key>
AMEDUS_API_KEY=<key>
AMEDUS_API_SECRET=<key>

## To get the Authorization Token for Ameadus:

1.) run the command in "run_command.txt", you should get a response like

{
            "type": "amadeusOAuth2Token",
            "username": "sbj3264@gmail.com",
            "application_name": "SI206_Project",
            "client_id": "4vvQPNk3Hj6WRHHCZy1QSqvZVgbncqA8",
            "token_type": "Bearer",
            "access_token": "yMFGqRVjvGbP6U03afnwVMWarR5g",
            "expires_in": 1799,
            "state": "approved",
            "scope": "
}

2.) then use the access token in this line, replacing only the string after Bearer with the access_token

    headers = {
    'Authorization': 'Bearer BJTt7l3MBln2oGkedVT7peVqDIdn'
    }

## Documentation

https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference

https://developer.accuweather.com/accuweather-locations-api/apis/get/locations/v1/cities/search

https://www.ccra.com/airport-codes/

