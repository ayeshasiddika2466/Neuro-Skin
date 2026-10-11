def add_scores(answers):
    total = 0
    for a in answers:
        total = total + a
    return total
print(add_scores([1, 2, 3, 4, 5]))

def severity (score):
    if score <= 4:
        return "minimal"
    elif score <= 9:
        return "mild"
    else:
        return "Higher"
print(severity(7))

facts = {"stress_level": "HIGH","quality_of_life_impact": "HIGH"}
if facts["stress_level"] == "HIGH" and facts["quality_of_life_impact"] == "HIGH":
    print("integrated_impact = elevated")