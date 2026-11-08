from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models.product import Product
from .errors import Conflict, NotFound
from .schemas import (
    ProductOut, ProductIn, ProductPatch, ReserveIn, 
    ProductQueryArgsSchema, ProductListOut
)

products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products", description="Operations on products")

@products_bp.get("")
@products_bp.arguments(ProductQueryArgsSchema, location="query")
@products_bp.response(200, ProductListOut)
def list_products(query_args):
    page = query_args.get("page", 1)
    size = query_args.get("size", 20)
    base = db.select(Product).where(Product.archived.is_(False))
    
    rows = db.session.execute(
        base.order_by(Product.id).offset((page-1) * size).limit(size)
    ).scalars().all()
    
    total = db.session.scalar(
        db.select(db.func.count()).select_from(Product).where(Product.archived.is_(False))
    )
    
    return {
        "items": rows,
        "page": page,
        "size": size,
        "total": total
    }

@products_bp.get("/<int:id>")
@products_bp.response(200, ProductOut)
def get_product(id):
    p = db.get_or_404(Product, id)
    if p.archived:
        raise NotFound(message="Product not found")
    return p

@products_bp.post("")
@products_bp.arguments(ProductIn)
@products_bp.response(201, ProductOut)
def create_product(body):
    p = Product(**body)
    db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Conflict(message="sku already exists")
    return p

@products_bp.patch("/<int:id>")
@products_bp.arguments(ProductPatch)
@products_bp.response(200, ProductOut)
def patch_product(body, id):
    p = db.get_or_404(Product, id)
    if p.archived:
        raise NotFound(message="Product not found")
        
    for k, v in body.items():
        setattr(p, k, v)
    db.session.commit()
    return p

@products_bp.delete("/<int:id>")
@products_bp.response(204)
def delete_product(id):
    p = db.get_or_404(Product, id)
    p.archived = True
    db.session.commit()
    return ""

@products_bp.post("/<int:id>/reserve")
@products_bp.arguments(ReserveIn)
@products_bp.response(200, ProductOut)
def reserve_product(body, id):
    p = db.get_or_404(Product, id)
    if p.archived:
        raise NotFound(message="Product not found")
        
    if p.qty_in_stock < body["qty"]:
        raise Conflict(message=f"only {p.qty_in_stock} left")
    
    p.qty_in_stock -= body["qty"]
    db.session.commit()
    return p
