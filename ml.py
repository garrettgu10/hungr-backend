from sklearn import tree

#product feature vector for each recipe
def reduce(recipes):
    next_feature_idx = 0
    ingredient_feature_idx = {}
    for recipe in recipes:
        for ingredient in recipe['ingredients']:
            if ingredient["name"] not in ingredient_feature_idx:
                ingredient_feature_idx[ingredient["name"]] = next_feature_idx
                next_feature_idx += 1

    feature_vectors = []
    for recipe in recipes:
        feature_vector = [-1] * len(ingredient_feature_idx)
        for ingredient in recipe['ingredients']:
            feature_vector[ingredient_feature_idx[ingredient["name"]]] = 1
        feature_vectors.append(feature_vector)

    return {
        "ingredient_feature_idx": ingredient_feature_idx,
        "feature_vectors": feature_vectors
    }

def recipe_to_feature_vector(recipe, ingredient_feature_idx):
    feature_vector = [-1] * len(ingredient_feature_idx)
    for ingredient in recipe['ingredients']:
        if ingredient["name"] in ingredient_feature_idx:
            feature_vector[ingredient_feature_idx[ingredient["name"]]] = 1
    return feature_vector

def predict(recipes, ratings, num_predictions):
    rated_recipes = []
    for rating in ratings:
        name = rating["name"]
        rated_recipes.append(recipes[name])

    reduced = reduce(rated_recipes)
    ingredient_feature_idx = reduced["ingredient_feature_idx"]
    feature_vectors = reduced["feature_vectors"]

    clf = tree.DecisionTreeRegressor()
    clf = clf.fit(feature_vectors, list(map(lambda x: x['rating'], ratings)))

    all_recipes = list(recipes.values())
    feature_vectors = list(map(lambda x: recipe_to_feature_vector(x, ingredient_feature_idx), all_recipes))

    predictions = clf.predict(feature_vectors)

    return list(
        map(lambda x: {**x[0], "score": x[1]}, 
            sorted(zip(all_recipes, predictions), key=lambda x: x[1], reverse=True)[:num_predictions]))
