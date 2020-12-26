def parseLine(line):
    keyphrase = ' (contains '
    stopIngredients = line.index(keyphrase)
    ingredients = line[:stopIngredients].split(' ')
    allergens = line.strip()[stopIngredients + len(keyphrase):-1].split(', ')
    return (ingredients, allergens)

def parseInputFile(inputfilename):
    foodsIngredients = []
    foodsAllergens = []
    with open(inputfilename) as f:
        for line in f:
            (ingredients, allergens) = parseLine(line)
            foodsIngredients.append(ingredients)
            foodsAllergens.append(allergens)
    return (foodsIngredients, foodsAllergens)    

def narrowDown(foodsIngredientsWithAllergen):
    intersection = foodsIngredientsWithAllergen[0]
    for i in range(1, len(foodsIngredientsWithAllergen)):
        intersection = [ing for ing in foodsIngredientsWithAllergen[i] if ing in intersection]
    return intersection

def unusedIngredients(foodsIngredients, foodsAllergens):
    uniqueAllergens = {}
    for i in range(len(foodsAllergens)):
        for allergen in foodsAllergens[i]:
            if allergen not in uniqueAllergens:
                uniqueAllergens[allergen] = []
            uniqueAllergens[allergen].append(i)

    usedIngredients = set()
    for allergen in uniqueAllergens:
        ingredientsSlice = []
        for ind in uniqueAllergens[allergen]:
            ingredientsSlice.append(foodsIngredients[ind])
        intersection = narrowDown(ingredientsSlice)
        for ingredient in intersection:
            usedIngredients.add(ingredient)
    
    unusedIngredients = set()
    for ingredients in foodsIngredients:
        for ingredient in ingredients:
            if ingredient not in usedIngredients:
                unusedIngredients.add(ingredient)
        
    return unusedIngredients

def numTimesInList(ingredients, foodsIngredients):
    numTimes = 0
    for food in foodsIngredients:
        for foodIngredient in food:
            if foodIngredient in ingredients:
                numTimes += 1
    return numTimes

(foodsIngredients, foodsAllergens) = parseInputFile('input21.txt')
unused = unusedIngredients(foodsIngredients, foodsAllergens)
print(unused)
print(numTimesInList(unused, foodsIngredients))

def singleAllergens(allergensToIngredients):
    out = {}
    for allergen in allergensToIngredients:
        if len(allergensToIngredients[allergen]) == 1:
            out[allergen] = allergensToIngredients[allergen][0]
    return out

def narrowed(foodsIngredients, foodsAllergens):
    uniqueAllergens = {}
    for i in range(len(foodsAllergens)):
        for allergen in foodsAllergens[i]:
            if allergen not in uniqueAllergens:
                uniqueAllergens[allergen] = []
            uniqueAllergens[allergen].append(i)

    narrowed = {}
    for allergen in uniqueAllergens:
        ingredientsSlice = []
        for ind in uniqueAllergens[allergen]:
            ingredientsSlice.append(foodsIngredients[ind])
        intersection = narrowDown(ingredientsSlice)
        narrowed[allergen] = intersection

    # eliminate within the list
    singles = singleAllergens(narrowed)
    maxIt = 1000
    while len(singles) < len(narrowed):
        for allergen in narrowed:
            if allergen not in singles:
                newIngredients = [ing for ing in narrowed[allergen] if ing not in singles.values()]
                narrowed[allergen] = newIngredients
        singles = singleAllergens(narrowed)
        maxIt += 1

    sortedAllergens = sorted(singles.keys())
    return ','.join([singles[s] for s in sortedAllergens])

print(narrowed(foodsIngredients, foodsAllergens))
