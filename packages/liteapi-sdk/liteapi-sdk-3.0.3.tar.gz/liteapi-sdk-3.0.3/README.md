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

## Available Methods

### `get_full_rates(data)`

**Description:** Fetches full rates for a list of hotel IDs based on search criteria, including room types, rates, and cancellation policies.

**Usage:**

```python
data = {
    "checkin": "2024-12-01",
    "checkout": "2024-12-05",
    "hotelIds": ["lp1897", "lp67890"],
    "guests": [{"adults": 2}],
    "guestNationality": "US"
}

response = api.get_full_rates(data)
print(response)
```

### `prebook(data)`

**Description:** Confirms availability of rates for a given offer ID, generates a prebook ID, and returns updated rate information.

**Usage:**

```python
prebook_data = {
    "offerId": "test_offer_id",
    "usePaymentSdk": False
}

response = api.prebook(prebook_data)
print(response)
```

### `book(data)`

**Description:** Confirms a booking using the prebook ID, rate ID, guest, and payment information. Returns booking details and confirmation.

**Usage:**

```python
booking_data = {
    "prebookId": "prebook_id",
    "rateId": "rate_id",
    "guest": {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com"
    },
    "payment": {
        "method": "ACC_CREDIT_CARD"
    }
}

response = api.book(booking_data)
print(response)
```

### `get_booking_list_by_guest_id(guest_id)`

**Description:** Retrieves a list of booking IDs for a given guest ID.

**Usage:**

```python
guest_id = "guest_id_example"
response = api.get_booking_list_by_guest_id(guest_id)
print(response)
```

### `retrieve_booking(booking_id)`

**Description:** Retrieves the status and details for a specific booking ID.

**Usage:**

```python
booking_id = "test_booking_id"
response = api.retrieve_booking(booking_id)
print(response)
```

### `cancel_booking(booking_id)`

**Description:** Requests cancellation of an existing confirmed booking.

**Usage:**

```python
booking_id = "test_booking_id"
response = api.cancel_booking(booking_id)
print(response)
```

### `get_cities_by_country_code(country_code)`

**Description:** Returns a list of city names from a specific country.

**Usage:**

```python
country_code = "US"
response = api.get_cities_by_country_code(country_code)
print(response)
```

### `get_currencies()`

**Description:** Returns all available currency codes along with their names and the list of supported countries.

**Usage:**

```python
response = api.get_currencies()
print(response)
```

### `get_hotels(country_code, city_name, offset=None, limit=None, longitude=None, latitude=None, distance=None)`

**Description:** Returns a list of hotels available based on different search criteria.

**Usage:**

```python
country_code = "US"
city_name = "New York"
response = api.get_hotels(country_code, city_name)
print(response)
```

### `get_hotel_details(hotel_id)`

**Description:** Returns all static content details of a hotel or property, including name, description, address, amenities, and images.

**Usage:**

```python
hotel_id = "lp1897"
response = api.get_hotel_details(hotel_id)
print(response)
```

### `get_hotel_reviews(hotel_id, limit)`

**Description:** Retrieves a list of reviews for a specific hotel identified by hotel ID.

**Usage:**

```python
hotel_id = "lp1897"
limit = 10
response = api.get_hotel_reviews(hotel_id, limit)
print(response)
```

### `get_countries()`

**Description:** Returns the list of available countries along with their ISO-2 codes.

**Usage:**

```python
response = api.get_countries()
print(response)
```

### `get_iata_codes()`

**Description:** Returns the IATA codes for all available airports along with their names, geographical coordinates, and country codes.

**Usage:**

```python
response = api.get_iata_codes()
print(response)
```

### `get_guests_ids(email="")`

**Description:** Returns the unique guest ID of a user based on the user's email ID.

**Usage:**

```python
email = "john.doe@example.com"
response = api.get_guests_ids(email=email)
print(response)
```

### `get_vouchers()`

**Description:** Retrieves all available vouchers.

**Usage:**

```python
response = api.get_vouchers()
print(response)
```

### `get_voucher_by_id(voucher_id)`

**Description:** Retrieves a voucher by its ID.

**Usage:**

```python
voucher_id = "voucher_id_example"
response = api.get_voucher_by_id(voucher_id)
print(response)
```

### `get_loyalty()`

**Description:** Fetches the current loyalty program information.

**Usage:**

```python
response = api.get_loyalty()
print(response)
```

### `get_places(text_query, place_type, language)`

**Description:**
Fetches a list of places based on a text query. The results can be filtered by place type and language.

**Parameters:**
- `text_query` (str): The text query to search for places. This parameter is required.
- `place_type` (str): The type of place to search for (optional).
- `language` (str): The language in which the results should be returned (optional).

**Usage:**

```python
response = api.get_places("hilton New York", "hotel", "en")
print(response)
```

### `get_hotel_facilities()`

**Description:**
Returns a list of hotel facilities available across hotels.

**Usage:**

```python
response = api.get_hotel_facilities()
print(response)
```

### `get_hotel_types()`

**Description:**
Returns a list of hotel types (e.g., resort, hotel, guesthouse) available.

**Usage:**

```python
response = api.get_hotel_types()
print(response)
```

### `get_hotel_chains()`

**Description:**
Returns a list of hotel chains.

**Usage:**

```python
response = api.get_hotel_chains()
print(response)
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