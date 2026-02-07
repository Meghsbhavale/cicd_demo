def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello World" in response.data.decode()


def test_health_route(client):
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "ok"
    assert json_data["version"] == "1.0"


def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2  # because we added 2 default items


def test_get_single_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1


def test_get_single_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404


def test_create_item(client):
    new_item = {"name": "Orange", "price": 0.9}
    response = client.post("/items", json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Orange"
    assert data["price"] == 0.9


def test_create_item_invalid(client):
    response = client.post("/items", json={"name": "BadItem"})
    assert response.status_code == 400


def test_error_route(client):
    response = client.get("/error")
    assert response.status_code == 500
