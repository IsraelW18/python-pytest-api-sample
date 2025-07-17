# tests/test_posts.py
from http.client import responses
from tests.conftest import logger
import pytest

class TestPostsAPI:

    def test_get_all_posts(self, api_client):
        response = api_client.get(endpoint="posts")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 100

    @pytest.mark.parametrize("post_id, expected_key", [
        (1, "title"),
        (10, "title"),
    ])
    def test_get_single_post(self, api_client, post_id, expected_key):
        response = api_client.get((f"posts/{post_id}"))
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert expected_key in data

    def test_create_post(self, api_client):
        payload = {
            "title": "qa title",
            "body": "qa body",
            "userId": 1
        }
        response = api_client.post(endpoint="posts", data=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "qa title"
        assert data["body"] == "qa body"

    def test_update_post(self, api_client):
        payload = {
            "title": "qa updated title"
        }
        response = api_client.patch(endpoint="posts/1", data=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "qa updated title"

    def test_delete_post(self, api_client):
        response = api_client.delete(endpoint="post/1")
        assert response.status_code in [200, 204]





