import asyncio
import json
from json.decoder import JSONDecodeError
from typing import Any, Coroutine, Dict, Generator, List, Optional, Union, Optional
from pydantic import ValidationError as VError
from starlette.concurrency import run_in_threadpool
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from models.exceptions import ValidationError
from importlib import import_module



class BaseHTTPEndpoint(HTTPEndpoint):
    validated_data = {}
    handler_name = ""
    api = None
    request_data = {}
    request = None

    def __await__(self) -> Generator:
        return self.dispatch().__await__()

    async def dispatch(self) -> None:

        await self.set_initial_data()
        response = await self.initial_validator()
        if response:
            await response(self.scope, self.receive, self.send)
            return
        handler = getattr(self, self.handler_name, self.method_not_allowed)
        is_async = asyncio.iscoroutinefunction(handler)
        if is_async:
            response = await handler(self.request)
        else:
            response = await run_in_threadpool(handler, self.request)
        await response(self.scope, self.receive, self.send)
        return

    async def initial_validator(self) -> Optional[Response]:
        try:
            await self.validator_method()
        except VError as e:
            return await self.get_error_response(e.errors(), "ValidationError")
        except ValidationError as e:
            return await self.get_error_response(
                json.loads(e.__str__()), "ValidationError"
            )
        except JSONDecodeError:
            pass
        except ValueError as e:
            return await self.get_error_response(e.__str__(), "ValidationError")

    async def get_database_api(self):
        from models.api.products_api import ProductAPI
        return ProductAPI(self.scope.get("database"))

    async def set_initial_data(self):
        self.api = await self.get_database_api()
        self.request = Request(self.scope, receive=self.receive)
        self.handler_name = "get" if self.request.method == "HEAD" else self.request.method.lower()
        self.request_data = await self.get_request_data(self.request)
        self.product_id = self.request.path_params.get("productId")

    async def get_request_data(self, request: Request) -> dict:
        data = {}
        data.update(request.query_params)
        try:
            data.update(await request.json())
        except JSONDecodeError:
            pass
        return data

    async def validator_method(self) -> None:
        data = self.request_data
        module = getattr(self, self.handler_name + "_validator_class", None)
        if module:
            validator_module = module.split(".")
            validator_class = validator_module[-1]
            validator_module.remove(validator_class)
            validator_pkg = ".".join(validator_module)
            validator_method = getattr(import_module(validator_pkg), validator_class)
            self.validated_data = validator_method(**data).dict()


    async def get_success_response(self, response: Union[dict, list]) -> JSONResponse:
        data = {"status": "success", "data": response}
        return JSONResponse(data)

    async def get_error_response(
        self, message: Any, code: str, log: bool = True, status_code=400
    ) -> JSONResponse:
        response = {
            "status": "error",
            "message": "unable to process request",
            "data": {"errors": {"origin": {"message": message, "code": code}}},
        }
        return JSONResponse(response, status_code)