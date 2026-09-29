from pydantic import BaseModel


class Product(BaseModel):
    product_id: str
    name: str
    manufacturer: str
    category: str
    ingredient_keyword: str
    concern: str
    report_number: str
    registered_on: str
    shelf_life: str | None
    appearance: str | None
    intake_method: str
    precautions: str | None
    functionality: str
    source_url: str | None
    data_source: str


class ProductList(BaseModel):
    total: int
    items: list[Product]
