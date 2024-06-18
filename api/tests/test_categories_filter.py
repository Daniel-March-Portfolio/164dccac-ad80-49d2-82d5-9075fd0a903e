import pytest


@pytest.mark.parametrize(
    "page,filters,count",
    [
        (0, {}, 3),
        (1, {}, 0),
        (0, {"title": "category 1"}, 1),
        (0, {"title": "category 2"}, 1),
        (0, {"title": "category 3"}, 1),
        (0, {"title__contains": "ategory"}, 3),
        (0, {"title__contains": "ategory 1"}, 1),
        (0, {"title__contains": "ategory 2"}, 1),
        (0, {"title__contains": "ategory 3"}, 1),
    ]
)
def test_categories_filter(app, client, page, filters, count):
    app.create_category(title="category 1")
    app.create_category(title="category 2")
    app.create_category(title="category 3")
    app.LIMIT = 5

    response = client.get("/api/v1/categories/filter/", params={"page": page, **filters})

    assert response.status_code == 200, response.text
    assert len(response.json()) == count
