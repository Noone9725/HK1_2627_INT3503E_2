import pytest
from src.product_api.factory import create_app
from src.product_api.extensions import db
from src.product_api.models.product import Product
from src.product_api.models.order import Order, OrderItem
from flask_sqlalchemy.record_queries import get_recorded_queries

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_RECORD_QUERIES": True # Bật cờ để đếm SQL
    })
    with app.app_context():
        db.create_all()
        # Seed data
        p1 = Product(sku="P1", name="Product 1", price_cents=1000, qty_in_stock=10)
        p2 = Product(sku="P2", name="Product 2", price_cents=2000, qty_in_stock=10)
        db.session.add_all([p1, p2])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_order(client):
    res = client.post("/api/v1/orders", json={
        "items": [
            {"product_id": 1, "qty": 2},
            {"product_id": 2, "qty": 5}
        ]
    })
    assert res.status_code == 201
    
    # Kiểm tra kho đã bị trừ
    p1 = db.session.get(Product, 1)
    assert p1.qty_in_stock == 8

def test_get_orders_n_plus_1(client, app):
    # Seed hóa đơn giả
    with app.app_context():
        for i in range(5):
            o = Order()
            o.items.append(OrderItem(product_id=1, qty=1, price_cents=1000))
            db.session.add(o)
        db.session.commit()

    with app.app_context():
        res = client.get("/api/v1/orders")
        assert res.status_code == 200
        
        queries = get_recorded_queries()
        # Số truy vấn phải luôn là hằng số (vd: 1 query Order + 2 query cho item/product)
        # Bất kể có 5 hay 50 hóa đơn, nếu vượt quá 4 query nghĩa là dính N+1
        assert len(queries) <= 4