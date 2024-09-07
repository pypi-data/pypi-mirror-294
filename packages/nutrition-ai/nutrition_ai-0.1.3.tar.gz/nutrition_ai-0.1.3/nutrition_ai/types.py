from pydantic import BaseModel, Field, RootModel


# Existing models from ProductCodeResponse
class Nutrient(BaseModel):
    name: str | None = None
    unit: str | None = None
    shortName: str | None = None
    group: str | None = None
    origin: list[dict[str, str]] | None = None


class NutrientInfo(BaseModel):
    id: int | None = None
    nutrient: Nutrient | None = None
    amount: float | None = None


class Weight(BaseModel):
    unit: str | None = None
    value: float | int | None = None


class Portion(BaseModel):
    weight: Weight | None = None
    name: str | None = None
    quantity: float | int | None = None
    suggestedQuantity: list[float] | None = None


class Image(BaseModel):
    bucket: str | None = None
    path: str | None = None


class Branded(BaseModel):
    owner: str | None = None
    productCode: str | None = None
    ingredients: str | None = None
    country: str | None = None
    certified: bool | None = None
    images: list[Image] | None = None
    ocrText: str | None = None
    reviewed: bool | None = None
    tested: bool | None = None
    upc: str | None = None


class Origin(BaseModel):
    source: str | None = None
    id: str | None = None
    dataType: str | None = None
    timestamp: str | None = None


# Base model for common fields
class BaseProductInfo(BaseModel):
    id: str | None = None
    name: str | None = None
    nutrients: list[NutrientInfo] | None = None
    portions: list[Portion]
    branded: Branded | None = None
    origin: list[Origin] | None = None
    qualityScore: str | None = None
    timestamp: str | None = None
    tags: list[str] | None = None
    refCode: str | None = None
    brandName: str | None = None
    description: str | None = None
    iconId: str | None = None
    licenseCopy: str | None = None
    name_i18n: dict[str, str] | None = None
    webLinks: list[str] | None = None


# ProductCodeResponse (previously APIResponse)
class ProductCodeResponse(BaseProductInfo):
    pass


class Alternative(BaseModel):
    displayName: str | None = None
    iconId: str | None = None
    labelId: str | None = None
    resultId: str | None = None
    type: str | None = None


class SearchResult(BaseModel):
    displayName: str | None = None
    iconId: str | None = None
    type: str | None = None
    refCode: str | None = None
    # Optional fields
    ingredients: list[dict] | None = None
    internalId: str | None = None
    internalName: str | None = None
    portions: list[dict] | None = None


class SearchResponse(BaseModel):
    results: list[SearchResult]
    alternatives: list[Alternative] | None = None


class ProductResponse(BaseModel):
    name: str | None = None
    fromViews: list[str] | dict | None = None
    nutrients: list[NutrientInfo] | None = None
    portions: list[Portion] | None = None
    branded: Branded | None = None
    timestamp: str | None = None
    tags: list[str] | None = None

    class Config:
        extra = "ignore"


class NutritionPreview(BaseModel):
    portion: Portion | None = None
    calories: float | None = None
    carbs: float | None = None
    fat: float | None = None
    protein: float | None = None
    fiber: float | None = None


class IngredientInfo(BaseModel):
    ingredientName: str | None = None
    portionSize: str | None = None
    portionQuantity: int | None = None
    weightGrams: float | None = None
    weightIsExplicit: bool | None = None
    type: str | None = None
    displayName: str | None = None
    stemmedDisplayName: str | None = None
    shortName: str | None = None
    longName: str | None = None
    scoredName: str | None = None
    score: float | None = None
    displayNameScore: float | None = None
    brandName: str | None = None
    iconId: str | None = None
    labelId: str | None = None
    synonymId: str | None = None
    recipeId: str | None = None
    referenceId: str | None = None
    resultId: str | None = None
    nutritionPreview: NutritionPreview | None = None
    refCode: str | None = None
    tags: list[str] | None = None


# The response is now a list of IngredientInfo objects
class IngredientResponse(RootModel):
    root: list[IngredientInfo]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
