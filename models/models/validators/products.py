from pydantic import BaseModel, constr


class UpdateProduct(BaseModel):
    name: constr(min_length=1) = ""
    brand_id: int = ""
    category_id: int


class CreateCategoryData(BaseModel):
    name: constr(min_length=1)
    description: constr(min_length=1)


class CreateBrandData(BaseModel):
    name: constr(min_length=1)
    description: constr(min_length=1)


class CreateProduct(BaseModel):
    name: constr(min_length=1)
    brand: CreateBrandData
    category: CreateCategoryData
