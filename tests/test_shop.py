def test_catalog_displays_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert b"Test Laptop" in response.data


def test_catalog_search_filters_products(client):
    assert b"Test Laptop" in client.get("/products?q=TestBrand").data
    assert b"Test Laptop" not in client.get("/products?q=Nonexistent").data


def test_missing_product_returns_404(client):
    assert client.get("/products/9999").status_code == 404

