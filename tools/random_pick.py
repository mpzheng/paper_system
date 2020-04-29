import random
def random_pick(probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item_probability in probabilities:
        cumulative_probability += item_probability
        if x < cumulative_probability:
            return probabilities.index(item_probability)