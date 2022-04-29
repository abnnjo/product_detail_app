import asyncio
import uuid
from gino.engine import GinoEngine
from sqlalchemy import text, delete, update, insert, func, select, exists
from typing import NoReturn, Dict
from ..exceptions import DataDoesNotExist, ValidationError
from sqlalchemy.engine.result import RowProxy
from ..db_models.product import Product, Brand, Category
from asyncpg.exceptions import ForeignKeyViolationError


class ProductAPI:
    def __init__(self, engine: GinoEngine) -> NoReturn:
        self.engine = engine

    async def get_product_detail(self, product_id: str) -> RowProxy:
        """
        This method used to return product details
        Args:
                - product_id(String): Product Id
        Returns:
                RowProxy contains product details
        """
        query = text(
            """
				select
					p.id,
					p.name,
					json_build_object('name', b."name", 'description', b.description) as brand,
					json_build_object('name', c."name", 'description', c.description) as category
				from
					product p
				left join brand b on
					b.id = p.brand_id
				left join category c on
					c.id = p.category_id 
				where
					p.id = :product_id			
			"""
        )
        result = await self.engine.first(query, product_id=product_id)
        if not result:
            raise DataDoesNotExist(
                f"Data does not exist for product with id '{product_id}'"
            )
        return dict(result)

    async def delete_product(self, product_id) -> bool:
        """
        This method is used to delete product
        """
        query = delete(Product).where(Product.id == product_id)
        result = await self.engine.status(query)
        if result and result[0] == "DELETE 0":
            raise DataDoesNotExist(
                f"Data does not exist for product with id '{product_id}'"
            )
        return True

    async def update_product_detail(self, product_id: str, data: Dict):
        """ """
        query = update(Product).where(Product.id == product_id).values(**data)
        try:
            result = await self.engine.status(query)
        except ForeignKeyViolationError as e:
            raise ValidationError(e.__str__())
        if result and result[0] == "UPDATE 0":
            raise DataDoesNotExist(
                f"Data does not exist for product with id '{product_id}'"
            )
        return True

    async def create_product(self, data: Dict):
        """ """
        category_data = data.pop("category")
        brand = data.pop("brand")
        product_id = f"pro_{uuid.uuid4().hex}"
        cat_id, bra_id = await asyncio.gather(
            self.create_category(category_data), self.create_brand(brand)
        )
        data.update({"category_id": cat_id, "brand_id": bra_id, "id": product_id})
        query = insert(Product).values(**data)
        result = await self.engine.status(query)
        if result and result[0] == "INSERT 0":
            raise ValidationError("Failed to insert data")
        return await self.get_product_detail(product_id)

    async def create_category(self, data) -> bool:
        """ """
        query = select([Category.id]).where(
            func.lower(Category.name) == data.get("name", "")
        )
        category_result = await self.engine.first(query)
        if not category_result:
            insert_query = insert(Category).values(**data).returning(Category.id)
            result = await self.engine.status(insert_query)
            if result and result[0] == "INSERT 0":
                raise ValidationError("Failed to insert data")
            else:
                category_id = result[1][0].id
        else:
            category_id = category_result.id
        return category_id

    async def create_brand(self, data) -> bool:
        """ """
        query = select([Brand.id]).where(func.lower(Brand.name) == data.get("name", ""))
        brand_result = await self.engine.first(query)
        if not brand_result:
            insert_query = insert(Brand).values(**data).returning(Brand.id)
            result = await self.engine.status(insert_query)
            if result and result[0] == "INSERT 0":
                raise ValidationError("Failed to insert data")
            else:
                brand_id = result[1][0].id
        else:
            brand_id = brand_result.id
        return brand_id
