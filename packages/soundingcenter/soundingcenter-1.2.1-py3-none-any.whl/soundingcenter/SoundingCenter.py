from requests import Response, get, post


class Api:
    def __init__(
        self, base_url: str, username: str, password: str, logging: bool = False
    ):
        self.base_url = base_url
        self.auth = (username, password)
        self.logging = logging

    def log(self, value):
        if self.logging:
            print(value)

    def log_response(self, response: Response):
        if self.logging and not response.ok:
            print(response.status_code)
            print(response.content)

    def get(self, path: str):
        self.log(f"GET {self.base_url}/{path}")

        request = get(
            url=f"{self.base_url}/{path}",
            headers={
                "Accept": "application/json",
            },
            auth=self.auth,
        )

        self.log_response(request)
        return request

    def post(self, path: str, json):
        self.log(f"POST {self.base_url}/{path} {json}")

        request = post(
            url=f"{self.base_url}/{path}",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            auth=self.auth,
            json=json,
        )

        self.log_response(request)
        return request

    def user(self):
        return self.get("user/self")

    def create_user(self, email: str, password: str, role: str, name: str):
        return self.post(
            "user",
            {
                "email": email,
                "password": password,
                "role": role,
                "name": name,
            },
        )

    def create_station(
        self,
        name: str,
        operation_type: str,
        wmo_id: int,
        latitude: float,
        longitude: float,
        altitude: float,
    ):
        return self.post(
            "station",
            {
                "name": name,
                "type": operation_type,
                "wmo_id": wmo_id,
                "latitude": latitude,
                "longitude": longitude,
                "altitude": altitude,
            },
        )

    def attach_station_to_user(self, user_id: int, station_id: int):
        return self.post(f"user/{user_id}/attachStation/{station_id}", {})
