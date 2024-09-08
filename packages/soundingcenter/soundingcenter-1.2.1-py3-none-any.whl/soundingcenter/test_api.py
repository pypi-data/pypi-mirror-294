import unittest
from os import getenv
from os.path import isfile, dirname, join

from dotenv import load_dotenv
from faker import Faker
from requests import codes

from SoundingCenter import Api


class TestApi(unittest.TestCase):
    def setUp(self):
        env_file = join(dirname(__file__), "../../.env")

        if not isfile(env_file):
            print("script can not start because .env file is missing")
            exit(1)

        load_dotenv(env_file)

        self.api = Api(
            getenv("SC_API_URL"),
            getenv("SC_ADMIN_USERNAME"),
            getenv("SC_ADMIN_PASSWORD"),
            True,
        )
        self.fake = Faker()

    def test_user(self):
        response = self.api.user()
        self.assertEqual(response.status_code, codes.ok)

    def test_create_user(self):
        response = self.api.create_user(
            self.fake.email(), self.fake.password(), "user", self.fake.name()
        )
        self.assertEqual(response.status_code, codes.created)

    def test_create_station(self):
        response = self.api.create_station(
            self.fake.name(),
            "operated_fixed",
            self.fake.random_int(10000, 99999),
            float(self.fake.latitude()),
            float(self.fake.longitude()),
            self.fake.random_int(min=0, max=8848),
        )
        self.assertEqual(response.status_code, codes.created)

    def test_attach_station_to_user(self):
        user = self.api.create_user(
            self.fake.email(), self.fake.password(), "user", self.fake.name()
        ).json()
        station = self.api.create_station(
            self.fake.name(),
            "operated_fixed",
            self.fake.random_int(10000, 99999),
            float(self.fake.latitude()),
            float(self.fake.longitude()),
            self.fake.random_int(min=0, max=8848),
        ).json()
        response = self.api.attach_station_to_user(
            user["data"]["id"], station["data"]["id"]
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
