import requests

class LiteApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.service_url = "https://api.liteapi.travel/v3.0"
        self.book_service_url = "https://book.liteapi.travel/v3.0"
        self.dashboard_url = "https://da.liteapi.travel"

    def _make_request(self, url, method='GET', headers=None, data=None):
        if headers is None:
            headers = {
                'accept': 'application/json',
                'content-type': 'application/json',
                'X-API-Key': self.api_key
            }

        response = requests.request(method, url, headers=headers, json=data)

        if not response.ok:
            return {"status": "failed", "error": response.json().get('error')}

        return {"status": "success", "data": response.json().get('data')}

    def get_full_rates(self, data):
        url = f"{self.service_url}/hotels/rates"
        return self._make_request(url, method='POST', data=data)

    def prebook(self, data):
        if not isinstance(data, dict) or not data.get('offerId'):
            return {"status": "failed", "errors": ["The offerId is required"]}

        url = f"{self.book_service_url}/rates/prebook"
        return self._make_request(url, method='POST', data=data)

    def book(self, data):
        url = f"{self.book_service_url}/rates/book"
        return self._make_request(url, method='POST', data=data)

    def get_booking_list_by_guest_id(self, guest_id):
        if not guest_id:
            return {"status": "failed", "errors": ["The guest ID is required"]}

        url = f"{self.book_service_url}/bookings?guestId={guest_id}"
        return self._make_request(url)

    def retrieve_booking(self, booking_id):
        if not booking_id:
            return {"status": "failed", "errors": ["The booking ID is required"]}

        url = f"{self.book_service_url}/bookings/{booking_id}"
        return self._make_request(url)

    def cancel_booking(self, booking_id):
        if not booking_id:
            return {"status": "failed", "errors": ["The booking ID is required"]}

        url = f"{self.book_service_url}/bookings/{booking_id}"
        return self._make_request(url, method='PUT')

    def get_cities_by_country_code(self, country_code):
        if not country_code:
            return {"status": "failed", "errors": ["The country code is required"]}

        url = f"{self.service_url}/data/cities?countryCode={country_code}"
        return self._make_request(url)

    def get_currencies(self):
        url = f"{self.service_url}/data/currencies"
        return self._make_request(url)

    def get_hotels(self, country_code, city_name, offset=None, limit=None, longitude=None, latitude=None, distance=None):
        if not country_code or not city_name:
            return {"status": "failed", "errors": ["Country code and city name are required"]}

        params = {
            'countryCode': country_code,
            'cityName': city_name,
            'offset': offset,
            'limit': limit,
            'longitude': longitude,
            'latitude': latitude,
            'distance': distance
        }
        params = {k: v for k, v in params.items() if v is not None}
        query = '&'.join([f"{key}={value}" for key, value in params.items()])
        url = f"{self.service_url}/data/hotels?{query}"
        return self._make_request(url)

    def get_hotel_details(self, hotel_id):
        if not hotel_id:
            return {"status": "failed", "errors": ["The Hotel code is required"]}

        url = f"{self.service_url}/data/hotel?hotelId={hotel_id}"
        return self._make_request(url)

    def get_hotel_reviews(self, hotel_id, limit):
        if not hotel_id:
            return {"status": "failed", "errors": ["The Hotel code is required"]}

        url = f"{self.service_url}/data/reviews?hotelId={hotel_id}&limit={limit}&timeout=5"
        return self._make_request(url)

    def get_countries(self):
        url = f"{self.service_url}/data/countries"
        return self._make_request(url)

    def get_iata_codes(self):
        url = f"{self.service_url}/data/iataCodes"
        return self._make_request(url)

    def get_places(self, text_query, place_type=None, language=None):
        if not text_query:
            return {"status": "failed", "errors": ["text_query is required"]}

        params = {
            'textQuery': text_query,
            'type': place_type,
            'language': language
        }
        params = {k: v for k, v in params.items() if v is not None}
        query = '&'.join([f"{key}={value}" for key, value in params.items()])
        url = f"{self.service_url}/data/places?{query}"
        return self._make_request(url)

    def get_hotel_facilities(self):
        url = f"{self.service_url}/data/facilities"
        return self._make_request(url)

    def get_hotel_types(self):
        url = f"{self.service_url}/data/hotelTypes"
        return self._make_request(url)

    def get_hotel_chains(self):
        url = f"{self.service_url}/data/chains"
        return self._make_request(url)

    def get_guests_ids(self, email=""):
        params = {'email': email} if email else {}
        query = '&'.join([f"{key}={value}" for key, value in params.items()])
        url = f"{self.service_url}/guests?{query}"
        return self._make_request(url)

    def get_vouchers(self):
        url = f"{self.dashboard_url}/vouchers"
        return self._make_request(url)

    def get_voucher_by_id(self, voucher_id):
        if not voucher_id or not isinstance(voucher_id, str):
            return {"status": "failed", "error": "The voucher ID is required and must be a string."}

        url = f"{self.dashboard_url}/vouchers/{voucher_id}"
        return self._make_request(url)

    def get_loyalty(self):
        url = f"{self.service_url}/loyalties/"
        return self._make_request(url)

def get_instance(api_key):
    return LiteApi(api_key)
