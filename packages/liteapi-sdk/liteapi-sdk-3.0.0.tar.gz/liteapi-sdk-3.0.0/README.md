# LiteAPI Python SDK

A Python SDK for interacting with the LiteAPI platform.

## Installation

```bash
pip install liteapi-sdk
```

## Usage

```python
from liteapi import LiteApi

api = LiteApi("your_api_key")
response = api.get_full_rates(data={...})
print(response)
```

## Full scenario

```python
# Initialize the LiteApi SDK
api = LiteApi('your_api_key')

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
    "timeout": 10
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
```

---

## Testing

```
python3 -m unittest discover tests
```

---

## Build the SDK and publish the package

```bash
pip install setuptools wheel
python3 setup.py sdist bdist_wheel
pip install twine
twine upload dist/*
```