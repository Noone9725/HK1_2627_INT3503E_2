from flask_smorest import Blueprint
from sqlalchemy.orm import selectinload
from ..extensions import db
from ..models.order import Order, OrderItem
from ..models.product import Product
from .errors import Conflict, NotFound
from .schemas import OrderIn, OrderOut, OrderListOut

orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders", description="Operations on orders")

@orders_bp.post("")
@orders_bp.arguments(OrderIn)
@orders_bp.response(201, OrderOut)
def create_order(body):
    item_requests = body.get("items", [])
    
    new_order = Order()
    db.session.add(new_order)
    
    for item in item_requests:
        product = db.session.get(Product, item["product_id"])
        if not product or product.archived:
            db.session.rollback()
            raise NotFound(message=f"Product {item['product_id']} not found")
        if product.qty_in_stock < item["qty"]:
            db.session.rollback()
            raise Conflict(message=f"Product {product.id} out of stock")
            
        product.qty_in_stock -= item["qty"]
        order_item = OrderItem(
            product_id=product.id,
            qty=item["qty"],
            price_cents=product.price_cents
        )
        new_order.items.append(order_item)

    db.session.commit()
    return new_order

@orders_bp.get("")
@orders_bp.response(200, OrderListOut)
def list_orders():
    stmt = db.select(Order).options(selectinload(Order.items).selectinload(OrderItem.product))
    orders = db.session.execute(stmt).scalars().all()
    return {"items": orders}

@orders_bp.delete("/<int:id>")
@orders_bp.response(204)
def delete_order(id):
    order = db.get_or_404(Order, id)
    db.session.delete(order)
    db.session.commit()
    return ""
