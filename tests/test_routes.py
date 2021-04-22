

def test_healthcheck(client):
    """Ensure the healthcheck endpoint returns a 200 (OK) status code."""
    with client as c:
        resp = client.get("/healthcheck")
        assert resp.status_code == 200