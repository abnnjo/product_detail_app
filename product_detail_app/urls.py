import time
from starlette.responses import JSONResponse
from .views.product import ProductEndpoint, CreateProduct


async def timestamp(request):
    return JSONResponse({"timestamp": time.time()})


url_patterns = [
    ("/time/", timestamp),
    ("/v1/product/{productId}/", ProductEndpoint),
    ("/v1/product/", CreateProduct),
]
