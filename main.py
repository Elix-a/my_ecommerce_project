from src.classes import Category, LawnGrass, Smartphone

if __name__ == "__main__":
    smartphone = Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        3.2,
        "S23 Ultra",
        256,
        "Серый",
    )
    grass = LawnGrass(
        "Трава газонная",
        "Универсальная",
        500.0,
        20,
        "Россия",
        14,
        "Зелёный",
    )

    print(smartphone)
    print(grass)

    smartphone2 = Smartphone(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
        3.0,
        "15",
        512,
        "Gray",
    )
    print(smartphone + smartphone2)

    try:
        print(smartphone + grass)
    except TypeError as e:
        print(f"Ошибка: {e}")

    category = Category("Телефоны", "Категория смартфонов", [smartphone, smartphone2])
    print(category)

    try:
        category.add_product("не продукт")  # type: ignore[arg-type]
    except TypeError as e:
        print(f"Ошибка: {e}")
