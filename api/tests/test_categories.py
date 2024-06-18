from uuid import uuid4


def test_get_category(client, category_manager):
    category_data = {"title": "title"}
    category_uuid = category_manager.create(**category_data)

    response = client.get(f"/api/v1/categories/{category_uuid}")
    assert response.status_code == 200, response.text
    assert response.json() == category_data


def test_get_category_not_found(client):
    response = client.get(f"/api/v1/categories/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.text == "Category not found"


def test_create_category(client, category_manager):
    category_data = {"title": "title"}
    response = client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == 201, response.text

    assert len(category_manager.filter(offset=0, limit=10)) == 1
    category_in_database_uuid = category_manager.filter(offset=0, limit=10)[0]
    assert response.text == str(category_in_database_uuid)


def test_update_category(client, category_manager):
    category_data = {"title": "title"}
    category_uuid = category_manager.create(**category_data)

    new_vales = {"title": "new title"}

    response = client.put(f"/api/v1/categories/{category_uuid}", json=new_vales)
    assert response.status_code == 200, response.text
    assert response.json() == new_vales


def test_update_category_without_passing_all_fields(client, category_manager):
    category_data = {"title": "title"}
    category_uuid = category_manager.create(**category_data)

    new_vales = {}

    response = client.put(f"/api/v1/categories/{category_uuid}", json=new_vales)
    assert response.status_code == 200, response.text
    category_data.update(new_vales)
    assert response.json() == category_data


def test_update_category_not_found(client):
    new_vales = {"title": "new title"}
    response = client.put(f"/api/v1/categories/{uuid4()}", json=new_vales)
    assert response.status_code == 404, response.text
    assert response.text == "Category not found"


def test_delete_category(client, category_manager):
    category_data = {"title": "title"}
    category_uuid = category_manager.create(**category_data)

    assert len(category_manager.filter(offset=0, limit=10)) == 1
    response = client.delete(f"/api/v1/categories/{category_uuid}")
    assert response.status_code == 204, response.text
    assert len(category_manager.filter(offset=0, limit=10)) == 0


def test_delete_category_not_found(client):
    response = client.delete(f"/api/v1/categories/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.text == "Category not found"
