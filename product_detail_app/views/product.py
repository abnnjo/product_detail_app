from starlette.requests import Request
from starlette.responses import JSONResponse
from models.exceptions import DataDoesNotExist, ValidationError
from ..http import BaseHTTPEndpoint
from ..utils import get_filter_validated_data


class ProductEndpoint(BaseHTTPEndpoint):
	patch_validator_class = "models.validators.products.UpdateProduct"
	async def get(self, request: Request) -> JSONResponse:
		"""
		This method is used to get products
		"""
		try:
			product = await self.api.get_product_detail(self.product_id)
		except DataDoesNotExist as e:
			return await self.get_error_response(e.__str__(), e.__class__.__name__)
		return await self.get_success_response(product)

	async def patch(self, request: Request) -> JSONResponse:
		"""
			This method used to update product details
		"""
		validated_data = get_filter_validated_data(self.request_data, self.validated_data)
		try:
			data = await self.api.update_product_detail(self.product_id, validated_data)
		except (DataDoesNotExist, ValidationError) as e:
			return await self.get_error_response(e.__str__(), e.__class__.__name__)
		validated_data["id"] = self.product_id
		return await self.get_success_response(validated_data)


	async def delete(self, request: Request) -> JSONResponse:
		"""
			This method is used to delete the product
		"""
		try:
			await self.api.delete_product(self.product_id)
		except DataDoesNotExist as e:
			return await self.get_error_response(e.__str__(), e.__class__.__name__)
		return await self.get_success_response({"product_id": self.product_id})


class CreateProduct(BaseHTTPEndpoint):
	post_validator_class = "models.validators.products.CreateProduct"
	async def post(self, request: Request) ->JSONResponse:
		"""
		"""
		try:
			product = await self.api.create_product(self.validated_data)
		except ValidationError as e:
			return await self.get_error_response(e.__str__(), e.__class__.__name__)
		return await self.get_success_response(product)

