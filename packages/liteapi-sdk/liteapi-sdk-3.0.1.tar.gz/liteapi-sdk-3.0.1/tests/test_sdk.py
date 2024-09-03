import unittest
from liteapi.sdk import LiteApi

class TestLiteApiReal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up with a real API key and other necessary setup
        cls.api_key = "sand_c0155ab8-c683-4f26-8f94-b5e92c5797b9"
        cls.api = LiteApi(cls.api_key)

        cls.test_hotel_id = "lp1897"

    def test_get_countries(self):
        response = self.api.get_countries()
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_cities_by_country_code(self):
        response = self.api.get_cities_by_country_code("US")
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_currencies(self):
        response = self.api.get_currencies()
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_hotels(self):
        response = self.api.get_hotels("US", "New York")
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_hotel_details(self):
        response = self.api.get_hotel_details(self.test_hotel_id)
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_hotel_reviews(self):
        response = self.api.get_hotel_reviews(self.test_hotel_id, limit=10)
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_iata_codes(self):
        response = self.api.get_iata_codes()
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_full_rates(self):
        response = self.api.get_full_rates({
            "checkin": "2024-12-01",
            "checkout": "2024-12-05",
            "hotelIds": [self.test_hotel_id],
            "occupancies": [{"adults": 2, "children": []}],
            "guestNationality": "US",
            "currency": "USD",
            "roomMapping": True
        })
        self.assertIn("data", response)

    def test_get_places(self):
        response = self.api.get_places("hilton New York", "hotel", "en")
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_hotel_facilities(self):
        response = self.api.get_hotel_facilities()
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_hotel_types(self):
        response = self.api.get_hotel_types()
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

    def test_get_hotel_chains(self):
        response = self.api.get_hotel_chains()
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)

if __name__ == '__main__':
    unittest.main()
