import requests
from datetime import datetime, timedelta
from liteapi import LiteApi

# Constants
API_KEY = 'sand_c0155ab8-c683-4f26-8f94-b5e92c5797b9'

# Initialize the LiteApi SDK
api = LiteApi(API_KEY)

def run_workflow():
    try:
        print("Running end-to-end testing workflow...")

        # Step 1: Fetch a list of hotels in New York, US
        hotels_response = api.get_hotels(country_code="US", city_name="New York", limit=200)
        hotels = hotels_response["data"]

        if not hotels:
            raise Exception("No hotels found")

        # Step 2: Fetch rates for the found hotels
        checkin_date = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
        checkout_date = (datetime.now() + timedelta(days=181)).strftime('%Y-%m-%d')

        rates_response = api.get_full_rates({
            "hotelIds": [hotel['id'] for hotel in hotels],
            "checkin": checkin_date,
            "checkout": checkout_date,
            "occupancies": [{"adults": 2}],
            "currency": "USD",
            "guestNationality": "US",
            "timeout": 5
        })

        rates = rates_response["data"]
        if not rates:
            raise Exception("No rates found")

        offer_id = rates[0]["roomTypes"][0]["offerId"]
        print(f"Found offer: {offer_id}")

        # Step 3: Make a prebooking request
        prebook_response = api.prebook({"offerId": offer_id, "usePaymentSdk": False})
        prebook_id = prebook_response["data"]["prebookId"]
        print(f"Prebooked with prebookId: {prebook_id}")

        # Step 4: Make a booking request
        booking_data = {
            "holder": {
                "firstName": "Uptime",
                "lastName": "Monitor",
                "email": "monitor@liteapi.travel"
            },
            "payment": {
                "method": "ACC_CREDIT_CARD"
            },
            "prebookId": prebook_id,
            "guests": [
                {
                    "occupancyNumber": 1,
                    "remarks": "quiet room please",
                    "firstName": "Uptime",
                    "lastName": "Monitor",
                    "email": "monitor@liteapi.travel"
                }
            ]
        }

        booking_response = api.book(booking_data)
        if booking_response["data"]["status"] != "CONFIRMED":
            raise Exception("Booking failed")

        # Step 5: Signal success
        print("Workflow passed")

    except Exception as error:
        print(f"Workflow failed: {error}")

# Run the workflow
run_workflow()