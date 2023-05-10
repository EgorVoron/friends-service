import pytest
import requests
import json


def decode(response_content):
    return json.loads(response_content.decode(encoding='utf-8'))


BASE_URL = "http://localhost:8000"
API_URL = BASE_URL + "/api/v1"

# register two test users
r = requests.post(BASE_URL + "/auth/register",
                  json={"username": "test0", "password": "test0"})
id_0 = decode(r.content)["id"]
r = requests.post(BASE_URL + "/auth/register",
              json={"username": "test1", "password": "test1"})
id_1 = decode(r.content)["id"]


def get_token(username="test0", password="test0"):
    r = requests.post(BASE_URL + "/auth/token/login", json={"username": username, "password": password})
    return decode(r.content)["token"]


def test_incoming():
    token = get_token()
    r = requests.get(API_URL + "/friends/requests/incoming", headers={"Authorization": f"Token {token}"})
    assert r.status_code == 204


def test_outgoing():
    token = get_token()
    r = requests.get(API_URL + "/friends/requests/outgoing", headers={"Authorization": f"Token {token}"})
    assert r.status_code == 204


def test_send():
    token = get_token()
    r = requests.post(API_URL + "/friends/requests/send", headers={"Authorization": f"Token {token}"},
                      data={'id': 5})
    assert r.status_code == 400

    r = requests.post(API_URL + "/friends/requests/send", headers={"Authorization": f"Token {token}"},
                      data={'id': id_1})
    assert r.status_code == 201

    r = requests.post(API_URL + "/friends/requests/send", headers={"Authorization": f"Token {token}"},
                      data={'id': id_1})
    assert r.status_code == 400  # already

    r = requests.get(API_URL + "/friends/requests/outgoing", headers={"Authorization": f"Token {token}"})
    assert r.status_code == 200
    response_json = decode(r.content)
    assert response_json[0]["id"] == id_1


def test_accept():
    token = get_token("test1", "test1")
    r = requests.post(API_URL + "/friends/requests/accept", headers={"Authorization": f"Token {token}"},
                      data={"id": id_0})
    assert r.status_code == 200


def test_get_all_friends():
    token = get_token()
    r = requests.get(API_URL + "/friends/all", headers={"Authorization": f"Token {token}"})
    assert r.status_code == 200
    response_json = decode(r.content)
    assert response_json[0]["id"] == id_1


def test_delete():
    token = get_token()
    r = requests.delete(API_URL + "/friends/delete", headers={"Authorization": f"Token {token}"},
                        data={"id": id_1})
    assert r.status_code == 200

    r = requests.get(API_URL + "/friends/all", headers={"Authorization": f"Token {token}"})
    assert r.status_code == 204


def test_check_status():
    token = get_token()
    r = requests.get(API_URL + "/friends/check_status", headers={"Authorization": f"Token {token}"},
                      data={"id": id_1})
    assert r.status_code == 200
    response_json = decode(r.content)
    assert response_json["message"] == "unrelated"
