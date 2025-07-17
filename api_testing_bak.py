from http.client import responses
import requests
import pytest


def get_url(post_id=''):
    return f"https://jsonplaceholder.typicode.com/posts/{post_id}"

def test_get_all_posts():
    url = get_url()
    print(url)
    response = requests.get(url)
    assert response.status_code == 200

    data = response.json()
    assert type(data) == list
    assert len(data) >= 100

@pytest.mark.parametrize("post_id, expected_type, expected_key",
                           [
                               ("10", dict, "title"),
                               ("99999", dict, "404")
                           ]
)
def test_get_posts_by_id(post_id, expected_type, expected_key):
    response = requests.get(get_url(post_id), verify=False)

    if post_id == "10":
        assert response.status_code == 200

        data = response.json()
        assert type(data) == expected_type

        _id = data["id"]
        assert _id == 10
        assert expected_key in data

    elif post_id == "9999":
        status_code = response.status_code
        assert status_code == 404, "status code is differs than '404'"
        print(f"status_code is '{status_code}'")

def test_delete_post():
    response = requests.delete(get_url("5"), verify=False)
    status_code = response.status_code
    assert status_code == 200 or 204, f"status code is {status_code}, instead of '200' or '204'"
    sec_response = requests.get(get_url("5"), verify=False)
    data = sec_response.json()
    print(f'\nThe post id is: {data["id"]}')


def test_update_title():
    url = get_url("1")
    response = requests.get(url, verify=False)
    data = response.json()
    print(f"\n\nExisting Title: {data["title"]}")

    payload = {"title" : "QA Title"}
    response = requests.patch(url, json=payload, verify=False)
    updated_data = response.json()
    assert updated_data["title"] == "QA Title"


def test_post_without_body():
    url = get_url("1")
    response = requests.post(url)