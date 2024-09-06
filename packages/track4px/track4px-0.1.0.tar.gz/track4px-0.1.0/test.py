from unittest import TestCase

from track4px import HTTPRequest, Track4PX

class TestHTTPRequest(TestCase):
    def test_http_request(self):
        http = HTTPRequest("https://httpbin.kumi.systems/get")
        response = http.execute()
        self.assertEqual(response["headers"]["User-Agent"], http.USER_AGENT)

class TestTrack4PX(TestCase):
    def setUp(self):
        self.api = Track4PX()

    def test_tracking(self):
        tracking_number = "4PX3001291278502CN"
        response = self.api.tracking(tracking_number, wrap=True)
        self.assertTrue(response.events)
        self.assertEqual(response.tracking_number, tracking_number)
