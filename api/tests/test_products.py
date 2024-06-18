from uuid import uuid4


def test_get_product(client, product_manager, category_manager):
    category_data = {"title": "title"}
    category_uuid = category_manager.create(**category_data)
    product_data = {
        "title": "title",
        "description": "description",
        "cost": 100,
        "category": category_uuid
    }
    product_uuid = product_manager.create(**product_data)

    response = client.get(f"/api/v1/products/{product_uuid}")
    assert response.status_code == 200, response.text
    product_data["category"] = category_data
    assert response.json() == product_data


def test_get_product_not_found(client):
    response = client.get(f"/api/v1/products/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.text == "Product not found"


def test_create_product(client, product_manager, category_manager):
    category_uuid = category_manager.create(**{"title": "title"})
    product_data = {
        "title": "title",
        "description": "description",
        "cost": 100,
        "category_uuid": str(category_uuid)
    }
    response = client.post("/api/v1/products/", json=product_data)
    assert response.status_code == 201, response.text

    assert len(product_manager.filter(offset=0, limit=10)) == 1
    product_in_database_uuid = product_manager.filter(offset=0, limit=10)[0]
    assert response.text == str(product_in_database_uuid)


def test_create_product_category_not_found(client, product_manager):
    product_data = {
        "title": "title",
        "description": "description",
        "cost": 100,
        "category_uuid": str(uuid4())
    }
    response = client.post("/api/v1/products/", json=product_data)
    assert response.status_code == 404, response.text
    assert response.text == "Category not found"
    assert len(product_manager.filter(offset=0, limit=10)) == 0


def test_update_product(client, product_manager, category_manager):
    category2_data = {"title": "title 2"}
    category1_uuid = category_manager.create(**{"title": "title 1"})
    category2_uuid = category_manager.create(**category2_data)
    product_data = {
        "title": "title",
        "description": "description",
        "cost": 100,
        "category": category1_uuid
    }
    product_uuid = product_manager.create(**product_data)

    new_vales = {
        "title": "new title",
        "description": "new description",
        "cost": 200,
        "category_uuid": str(category2_uuid)
    }

    response = client.put(f"/api/v1/products/{product_uuid}", json=new_vales)
    assert response.status_code == 200, response.text
    new_vales["category"] = category2_data
    del new_vales["category_uuid"]
    assert response.json() == new_vales


def test_update_product_without_passing_all_fields(client, product_manager, category_manager):
    category2_data = {"title": "title 2"}
    category1_uuid = category_manager.create(**{"title": "title 1"})
    category2_uuid = category_manager.create(**category2_data)
    product_data = {
        "title": "title",
        "description": "description",
        "cost": 100,
        "category": category1_uuid
    }
    product_uuid = product_manager.create(**product_data)

    new_vales = {
        "title": "new title",
        "category_uuid": str(category2_uuid)
    }

    response = client.put(f"/api/v1/products/{product_uuid}", json=new_vales)
    assert response.status_code == 200, response.text
    product_data.update(new_vales)
    product_data["category"] = category2_data
    del product_data["category_uuid"]
    assert response.json() == product_data


def test_update_product_not_found(client):
    new_vales = {
        "title": "new title",
        "description": "new description",
        "cost": 200,
        "category_uuid": str(uuid4())
    }
    response = client.put(f"/api/v1/products/{uuid4()}", json=new_vales)
    assert response.status_code == 404, response.text
    assert response.text == "Product not found"


def test_delete_product(client, product_manager, category_manager):
    category_uuid = category_manager.create(**{"title": "title"})
    product_data = {
        "title": "title",
        "description": "description",
        "cost": 100,
        "category": category_uuid
    }
    product_uuid = product_manager.create(**product_data)

    assert len(product_manager.filter(offset=0, limit=10)) == 1
    response = client.delete(f"/api/v1/products/{product_uuid}")
    assert response.status_code == 204, response.text
    assert len(product_manager.filter(offset=0, limit=10)) == 0


def test_delete_product_not_found(client):
    response = client.delete(f"/api/v1/products/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.text == "Product not found"
