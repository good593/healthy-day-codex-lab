from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.api.dependencies import get_product_service
from backend.schemas.products import Product, ProductList
from backend.services.products import ProductNotFoundError, ProductService

router = APIRouter(prefix="/products", tags=["products"])
Service = Annotated[ProductService, Depends(get_product_service)]


@router.get("", response_model=ProductList)
def list_products(
    service: Service,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> ProductList:
    return service.list_products(limit=limit, offset=offset)


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str, service: Service) -> Product:
    try:
        return service.get_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(404, "상품을 찾을 수 없습니다.") from exc
