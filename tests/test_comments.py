# /tests/test_comments.py
import pytest

class TestCommentsAPI:

    @pytest.mark.get
    @pytest.mark.comments
    @pytest.mark.positive
    @pytest.mark.integration
    def test_get_all_comments(self, api_client, logger):
        logger.info("running test: get all comments")
        response = api_client.get(endpoint="comments")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    @pytest.mark.get
    @pytest.mark.comments
    @pytest.mark.positive
    @pytest.mark.integration
    @pytest.mark.parametrize("comment_id, expected_key", [
        (1, "email"),
        (50, "name"),
    ])
    def test_get_single_comment(self, api_client, logger, comment_id, expected_key):
        logger.info("running test: test_get_single_comment")
        response = api_client.get(endpoint=f"comments/{comment_id}")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)
        assert expected_key in data

    @pytest.mark.post
    @pytest.mark.comments
    @pytest.mark.positive
    @pytest.mark.integration
    @pytest.mark.regression
    def test_create_comment(self, api_client, logger):
        logger.info("running test: test_create_comment")
        payload = {
            "postId": 1,
            "name": "QA comment Test",
            "email": "qa@example.com",
            "body": "QA This is a test comment"
        }
        response = api_client.post(endpoint="comments", data=payload)
        assert response.status_code == 201

        data = response.json()
        for key, value in payload.items():
            assert data[key] == value, logger.info(f"Assertion Error: response value '{data[key]}' != {value}")

    @pytest.mark.patch
    @pytest.mark.comments
    @pytest.mark.positive
    @pytest.mark.integration
    @pytest.mark.regression
    def test_update_comment(self, api_client, logger):
        logger.info("running test: test_update_comment")
        payload = {
            "body": "QA Update comment body"
        }
        response = api_client.patch(endpoint="comments/1", data=payload)
        assert response.status_code == 200
        data = response.json()

        body = data["body"]
        assert body == "QA Update comment body"

    @pytest.mark.delete
    @pytest.mark.comments
    @pytest.mark.positive
    @pytest.mark.integration
    @pytest.mark.regression
    def test_delete_comment(self, api_client, logger):
        logger.info("running test: test_delete_comment")
        response = api_client.delete(endpoint="comments/1")
        if response.text:
            assert response.status_code == 200
        else:
            assert response.status_code == 204
