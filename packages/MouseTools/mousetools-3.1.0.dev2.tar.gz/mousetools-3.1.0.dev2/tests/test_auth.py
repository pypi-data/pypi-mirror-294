from mousetools import auth


def test_auth():
    headers = auth.auth_obj.get_headers()
    assert headers

    assert headers["Authorization"] == f"BEARER {auth.auth_obj.access_token}"
