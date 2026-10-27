from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# Автоматически создаем таблицы в базе данных при запуске приложения
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cookbook API",
    description="Максимально подробное API кулинарной книги для фронтенд-разработчиков.",
    version="1.0.0"
)


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeShortResponse],
    summary="Получить список всех рецептов",
    description="Возвращает краткую информацию для первого экрана. Сортировка: сначала по популярности (views DESC), затем по времени приготовления (cooking_time ASC)."
)
def get_recipes(db: Session = Depends(get_db)):
    # Сортировка по убыванию просмотров (.desc()), затем по возрастанию времени приготовления
    recipes = db.query(models.Recipe).order_by(
        models.Recipe.views.desc(),
        models.Recipe.cooking_time.asc()
    ).all()
    return recipes


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeDetailResponse,
    summary="Получить детальную информацию о конкретном рецепте",
    description="Возвращает полную информацию для второго экрана. При каждом успешном запросе счетчик просмотров увеличивается на 1."
)
def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рецепт с id {recipe_id} не найден"
        )

    # Увеличиваем количество просмотров согласно ТЗ
    recipe.views += 1
    db.commit()
    db.refresh(recipe)

    return recipe


@app.post(
    "/recipes",
    response_model=schemas.RecipeDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый рецепт",
    description="Добавляет новый рецепт в кулинарную книгу. По умолчанию количество просмотров устанавливается в 0."
)
def create_recipe(recipe_data: schemas.RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = models.Recipe(
        title=recipe_data.title,
        cooking_time=recipe_data.cooking_time,
        ingredients=recipe_data.ingredients,
        description=recipe_data.description
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe
