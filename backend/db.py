from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "maralym.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    badge: Optional[str] = None
    image: Optional[str] = None
    price: int
    description: Optional[str] = None
    tags: Optional[str] = None  # comma-separated sizes
    rating: float = 0.0


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)


def list_products(category: Optional[str] = None) -> List[Product]:
    with get_session() as s:
        q = select(Product)
        if category and category != "all":
            q = q.where(Product.category == category)
        return list(s.exec(q).all())


def get_product_by_id(product_id: int) -> Optional[Product]:
    with get_session() as s:
        return s.get(Product, product_id)


def create_product(obj: dict) -> Product:
    with get_session() as s:
        p = Product(
            name=obj.get("name"),
            category=obj.get("category"),
            badge=obj.get("badge"),
            image=obj.get("image"),
            price=int(obj.get("price", 0)),
            description=obj.get("description", ""),
            tags=",".join(obj.get("tags", [])) if isinstance(obj.get("tags"), list) else obj.get("tags"),
            rating=float(obj.get("rating", 0.0)),
        )
        s.add(p)
        s.commit()
        s.refresh(p)
        return p


def update_product(product_id: int, data: dict) -> Optional[Product]:
    with get_session() as s:
        p = s.get(Product, product_id)
        if not p:
            return None
        for k, v in data.items():
            if k == "tags" and isinstance(v, list):
                setattr(p, k, ",".join(v))
            elif hasattr(p, k):
                setattr(p, k, v)
        s.add(p)
        s.commit()
        s.refresh(p)
        return p


def delete_product(product_id: int) -> bool:
    with get_session() as s:
        p = s.get(Product, product_id)
        if not p:
            return False
        s.delete(p)
        s.commit()
        return True
