import pytest


@pytest.mark.parametrize(
    "page,filters,count",
    [
        (0, {}, 3),
        (1, {}, 0),
        (0, {"title": "product 1"}, 1),
        (0, {"title": "product 2"}, 1),
        (0, {"title": "product 3"}, 1),
        (0, {"title__contains": "product"}, 3),
        (0, {"title__contains": "product 1"}, 1),
        (0, {"title__contains": "product 2"}, 1),
        (0, {"title__contains": "product 3"}, 1),
        (0, {"title__not_in": ["product 1", "product 2"]}, 1),
        (0, {"description": "description"}, 0),
        (0, {"description": "description 1"}, 1),
        (0, {"description__contains": "description"}, 3),
        (0, {"description__contains": "1"}, 1),
        (0, {"cost": 100}, 1),
        (0, {"cost__greater_than": 200}, 1),
        (0, {"cost__greater_than_or_equal_to": 200}, 2),
        (0, {"cost__lower_than": 100}, 0),
        (0, {"cost__lower_than_or_equal_to": 100}, 1),
        (0, {"cost__not_in": [100, 300]}, 1),
        (0, {"cost__in": [100]}, 1),
        (0, {"cost__not_equal": 100}, 2),
    ]
)
def test_products_filter(app, client, page, filters, count):
    category1_uuid = app.create_category(title="category 1")
    category2_uuid = app.create_category(title="category 2")

    app.create_product(title="product 1", description="description 1", cost=100, category_uuid=category1_uuid)
    app.create_product(title="product 2", description="description 2", cost=200, category_uuid=category1_uuid)
    app.create_product(title="product 3", description="description 3", cost=300, category_uuid=category2_uuid)
    app.LIMIT = 5

    response = client.get("/api/v1/products/filter/", params={"page": page, **filters})

    assert response.status_code == 200, response.text
    assert len(response.json()) == count
