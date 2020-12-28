from abc import ABC

from flask_testing import TestCase
from dashboard import create_app

class TestApi(TestCase, ABC):
    ## create app function retuns the app with context
    def create_app(self):
        return create_app()

    # call the /count endoint and check the return json
    def test_assert_count_api(self):
        response = self.client.get("/count")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.__contains__('tweets_count'),True)

    # call the top100 endpoint and check teh response
    def test_assert_top100(self):
        response = self.client.get("/top100")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.__contains__('tweets'),True)


    # call the /count endoint and check the return json
    def test_assert_mycount_api(self):
        response = self.client.get("/mycount")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.__contains__('tweets_count'),True)

    # call the top100 endpoint and check teh response
    def test_assert_mycount10_api(self):
        response = self.client.get("/mycount_ten")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.__contains__('tweets_count'),True)
