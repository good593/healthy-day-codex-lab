import sqlite3

from backend.schemas.products import Product


class ProductRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def list_products(self, *, limit: int, offset: int) -> tuple[int, list[Product]]:
        total = self.connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        rows = self.connection.execute(
            "SELECT * FROM products ORDER BY product_id LIMIT ? OFFSET ?", (limit, offset)
        ).fetchall()
        return total, [Product.model_validate(dict(row)) for row in rows]

    def get_product(self, product_id: str) -> Product | None:
        row = self.connection.execute(
            "SELECT * FROM products WHERE product_id = ?", (product_id,)
        ).fetchone()
        return Product.model_validate(dict(row)) if row else None
