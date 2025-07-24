# tests/test_users
import pytest

class TestUsersAPI:

    @pytest.mark.get
    @pytest.mark.users
    @pytest.mark.positive
    @pytest.mark.integration
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

    @pytest.mark.get
    @pytest.mark.users
    @pytest.mark.positive
    @pytest.mark.integration
    @pytest.mark.parametrize("user_id, expected_key", [
        (1, "name"),
        (5, "email"),
        (8, "username"),
    ])
    def test_get_single_user(self, api_client, logger, user_id, expected_key):
        logger.info(f"Running test: get single user 'user_id' = {user_id}")
        response = api_client.get(f"users/{user_id}")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)
        assert expected_key in data
        assert isinstance(data[expected_key], str)

    @pytest.mark.post
    @pytest.mark.users
    @pytest.mark.positive
    @pytest.mark.integration
    @pytest.mark.regression
    def test_create_user(self, api_client, logger):
        logger.info("Running test: create user")
        payload = {
            "name": "QA User",
            "username": "qauser",
            "email": "qauser@example.com",
            "phone": "123-456-7890",
            "website": "qauser.com"
        }
        response = api_client.post("users", data=payload)
        assert response.status_code == 201

        data = response.json()
        for key in payload:
            assert key in data.keys()
            assert data[key] == payload[key]

    @pytest.mark.put
    @pytest.mark.users
    @pytest.mark.positive
    @pytest.mark.integration
    @pytest.mark.regression
    def test_update_user_put(self, api_client, logger):
        logger.info("Running test: update user 'put'")
        payload = {
            "id": 1,
            "name": "QA Updated User",
            "username": "qa_updateduser",
            "email": "qa_updated@example.com",
            "phone": "999-999-9999",
            "website": "qa_updatedsite.com"
        }
        response = api_client.put("users/1", data=payload)
        assert response.status_code == 200
        data = response.json()
        assert all(data.get(k) == v for k, v in payload.items())

    @pytest.mark.patch
    @pytest.mark.users
    @pytest.mark.positive
    @pytest.mark.integration
    @pytest.mark.regression
    def test_update_user_patch(self, api_client, logger):
        logger.info("Running test: update user 'patch'")
        payload = {
            "email": "qa_patched@example.com"
        }
        response = api_client.patch("users/1", data=payload)
        assert response.status_code == 200

        data = response.json()
        assert "email" in data
        assert data["email"] == "qa_patched@example.com"

    @pytest.mark.delete
    @pytest.mark.users
    @pytest.mark.positive
    @pytest.mark.integration
    @pytest.mark.regression
    def test_delete_user(self,api_client, logger):
        logger.info("Running test: delete user")
        response = api_client.delete("users/1")
        if response.text:
            assert response.status_code == 200

        else:
            assert response.status_code == 204

