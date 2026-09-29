from backend.repositories.products import ProductRepository
from backend.schemas.products import Product, ProductList


class ProductNotFoundError(Exception):
    pass


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_products(self, *, limit: int, offset: int) -> ProductList:
        total, items = self.repository.list_products(limit=limit, offset=offset)
        return ProductList(total=total, items=items)

    def get_product(self, product_id: str) -> Product:
        product = self.repository.get_product(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product
