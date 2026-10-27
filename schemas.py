from pydantic import BaseModel, Field

# Базовая схема со всеми общими полями
class RecipeBase(BaseModel):
    title: str = Field(..., example="Борщ украинский", description="Название блюда")
    cooking_time: int = Field(..., example=60, description="Время приготовления в минутах")
    ingredients: str = Field(..., example="Свекла, капуста, картофель, говядина", description="Список ингредиентов")
    description: str = Field(..., example="Классический рецепт наваристого борща...", description="Текстовое описание")

# Схема для создания нового рецепта через POST
class RecipeCreate(RecipeBase):
    pass

# Схема для ПЕРВОГО ЭКРАНА (Краткая информация в списке)
class RecipeShortResponse(BaseModel):
    title: str = Field(..., description="Название блюда")
    views: int = Field(..., description="Количество просмотров")
    cooking_time: int = Field(..., description="Время приготовления в минутах")

    class Config:
        from_attributes = True

# Схема для ВТОРОГО ЭКРАНА (Детальная информация о рецепте)
class RecipeDetailResponse(BaseModel):
    title: str = Field(..., description="Название блюда")
    cooking_time: int = Field(..., description="Время приготовления в минутах")
    ingredients: str = Field(..., description="Список ингредиентов")
    description: str = Field(..., description="Текстовое описание")

    class Config:
        from_attributes = True
