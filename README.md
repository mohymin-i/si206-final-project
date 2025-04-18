To get the Authorization Token for Ameadus:

run the command in "run_command.txt", you should get a response like

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

then use the access token in this line, replacing only the string after Bearer with the access_token

    headers = {
    'Authorization': 'Bearer BJTt7l3MBln2oGkedVT7peVqDIdn'
    }

Documentation

https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference

https://developer.accuweather.com/accuweather-locations-api/apis/get/locations/v1/cities/search

https://www.ccra.com/airport-codes/

