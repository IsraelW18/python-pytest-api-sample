# tests/test_users
from itertools import count

import pytest

class TestUsersAPI:

    def test_get_all_users(self, api_client, logger):
        logger.info("Running Test: get all users")
        response = api_client.get("users")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 10

        users_count = 0
        for user in data:
            users_count += 1
            print(f"Testing user No: {users_count}")

            assert isinstance(user["id"], int)
            assert isinstance(user["name"], str)
            assert isinstance(user["username"], str)
            assert "@" in user["email"]
            assert isinstance(user["address"], dict)

            address = user["address"]
            assert isinstance(address["street"], str)
            assert isinstance(address["suite"], str)
            assert isinstance(address["city"], str)
            assert isinstance(address["zipcode"], str)
            assert isinstance(address["geo"], dict)

            geo = address["geo"]
            lat = float(geo["lat"])
            lng = float(geo["lng"])
            assert not lat == 0.0
            assert not lng == 0.0

            assert isinstance(user["phone"], str) and len(user["phone"]) >= 9
            assert isinstance(user["website"], str)

            company = user["company"]
            assert isinstance(company["name"], str)
            assert company["catchPhrase"] != ''
            assert isinstance(company["bs"], str)
