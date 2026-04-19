from utils import haversine_distance

def calculate_score(donor, receiver):
    # Priority 1: Children > Elderly
    child_score = receiver["people"]["children"] * 2 + receiver["people"]["elderly"]

    # Priority 2: Allergy filtering
    donor_ingredients = [ingredient.lower() for ingredient in donor["Ingredients"]]  # Lowercase each ingredient
    allergies = [a.strip().lower() for a in receiver["allergies"]]
    allergic = any(allergen in donor_ingredients for allergen in allergies)
    allergy_score = 0 if allergic else 1

    # Priority 3: Portion match
    portion_score = min(donor["Quantity"], receiver["required_portions"]) / receiver["required_portions"]

    # Priority 4: Distance (closer is better)
    distance = haversine_distance(
        (donor["latitude"], donor["longitude"]),
        (receiver["latitude"], receiver["longitude"])
    )

    # Inverse distance score: closer gets more score
    distance_score = 1 / (1 + distance)  # Avoid division by zero

    # Total Score (weights based on priority)
    total_score = (
        2 * child_score +
        1.5 * allergy_score +
        1.2 * portion_score +
        0.5 * distance_score
    )

    return total_score, distance

def match_donor_to_best_receiver(donor, receivers):
    best_receiver = None
    best_score = -1
    best_distance = float("inf")

    for receiver in receivers:
        score, distance = calculate_score(donor, receiver)
        if score > best_score:
            best_score = score
            best_receiver = receiver
            best_distance = distance
    
    return best_receiver, best_score, best_distance
