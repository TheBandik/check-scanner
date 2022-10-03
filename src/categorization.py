from fuzzywuzzy import fuzz

import db


# Определение категории товара
def category_detection(product):
    # Получение категорий из БД
    categories = db.get_categories()

    # Определение категории на основе нечёткого поиска 5 способами
    probs = []
    for category in categories:
        prob1 = fuzz.ratio(category[2], product)
        prob2 = fuzz.partial_ratio(category[2], product)
        prob3 = fuzz.token_sort_ratio(category[2], product)
        prob4 = fuzz.token_set_ratio(category[2], product)
        prob5 = fuzz.WRatio(category[2], product)

        probs.append(max(prob1, prob2, prob3, prob4, prob5))

    return categories[probs.index(max(probs))][0]
