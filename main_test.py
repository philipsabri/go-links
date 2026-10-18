import main
from fastapi.testclient import TestClient

client = TestClient(main.app)


def test_redirect(monkeypatch):
    main.config.clear()
    monkeypatch.setitem(main.config, "gh", "github.com")

    response = client.get("/gh", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "https://github.com"


def test_missing_redirect_is_404():
    main.config.clear()

    response = client.get("/missing", follow_redirects=False)

    assert response.status_code == 404
