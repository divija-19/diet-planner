from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# Your food data with goals
food_data_ml = [
    {"name": "Boiled Egg", "calories": 78, "protein": 6, "carbs": 0.6, "fat": 5.3, "goal": "weight gain"},
    {"name": "Grilled Chicken Breast", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "goal": "weight loss"},
    {"name": "Brown Rice (1 cup)", "calories": 216, "protein": 5, "carbs": 45, "fat": 1.8, "goal": "maintain"},
    {"name": "Oats (1/2 cup)", "calories": 150, "protein": 5, "carbs": 27, "fat": 3, "goal": "weight gain"},
    {"name": "Almonds (10 pieces)", "calories": 70, "protein": 2.6, "carbs": 2.5, "fat": 6.1, "goal": "weight gain"},
    {"name": "Apple", "calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3, "goal": "maintain"},
    {"name": "Greek Yogurt (1 cup)", "calories": 100, "protein": 10, "carbs": 6, "fat": 0, "goal": "weight loss"},
    {"name": "Sweet Potato (100g)", "calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1, "goal": "weight loss"},
    {"name": "Peanut Butter (2 tbsp)", "calories": 190, "protein": 8, "carbs": 6, "fat": 16, "goal": "weight gain"},
    {"name": "Salmon (100g)", "calories": 208, "protein": 20, "carbs": 0, "fat": 13, "goal": "weight loss"}
]

def train_model(food_data):
    X = []
    y = []
    for item in food_data:
        X.append([item['calories'], item['protein'], item['fat'], item['carbs']])
        y.append(item['goal'])
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def get_activity_multiplier(activity_level):
    activity_map = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9
    }
    return activity_map.get(activity_level.lower(), 1.2)

def generate_diet_plan(goal, calories):
    if goal.lower() == 'weight loss':
        calories -= 500
    elif goal.lower() == 'weight gain':
        calories += 500
    return calories

def calculate_macros(calories):
    protein = (0.3 * calories) / 4
    fats = (0.25 * calories) / 9
    carbs = (0.45 * calories) / 4
    return round(protein), round(fats), round(carbs)

def suggest_meals_ml(model, calorie_limit, protein_goal, fat_goal, carb_goal, user_goal):
    total_cal, total_protein, total_fat, total_carbs = 0, 0, 0, 0
    selected_items = {}
    max_servings_per_food = 4
    sorted_foods = sorted(food_data_ml, key=lambda x: x['calories'], reverse=True)

    while total_cal < calorie_limit * 0.95:
        added = False
        for food in sorted_foods:
            features = [[food['calories'], food['protein'], food['fat'], food['carbs']]]
            predicted_goal = model.predict(features)[0]
            if predicted_goal.lower() == user_goal.lower():
                count = selected_items.get(food["name"], {}).get("count", 0)
                if count >= max_servings_per_food:
                    continue

                new_protein = total_protein + food["protein"]
                new_fat = total_fat + food["fat"]
                new_carbs = total_carbs + food["carbs"]

                if (new_protein <= protein_goal * 1.5 and
                    new_fat <= fat_goal * 1.5 and
                    new_carbs <= carb_goal * 1.5 and
                    total_cal + food["calories"] <= calorie_limit):

                    if food["name"] in selected_items:
                        selected_items[food["name"]]["count"] += 1
                    else:
                        selected_items[food["name"]] = food.copy()
                        selected_items[food["name"]]["count"] = 1

                    total_cal += food["calories"]
                    total_protein += food["protein"]
                    total_fat += food["fat"]
                    total_carbs += food["carbs"]
                    added = True
                    break
        if not added:
            break

    # Fallback to add any food if calories not reached
    while total_cal < calorie_limit * 0.95:
        added = False
        for food in sorted_foods:
            count = selected_items.get(food["name"], {}).get("count", 0)
            if count >= max_servings_per_food:
                continue
            if total_cal + food["calories"] <= calorie_limit:
                if food["name"] in selected_items:
                    selected_items[food["name"]]["count"] += 1
                else:
                    selected_items[food["name"]] = food.copy()
                    selected_items[food["name"]]["count"] = 1

                total_cal += food["calories"]
                total_protein += food["protein"]
                total_fat += food["fat"]
                total_carbs += food["carbs"]
                added = True
                break
        if not added:
            break

    return selected_items, total_cal, total_protein, total_carbs, total_fat

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        age = int(request.form['age'])
        gender = request.form['gender']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        activity_level = request.form['activity_level']
        goal = request.form['goal']

        bmr = calculate_bmr(weight, height, age, gender)
        tdee = bmr * get_activity_multiplier(activity_level)
        final_calories = generate_diet_plan(goal, tdee)
        protein, fats, carbs = calculate_macros(final_calories)

        model = train_model(food_data_ml)
        selected_items, total_cal, total_protein, total_carbs, total_fat = suggest_meals_ml(
            model, final_calories, protein, fats, carbs, goal
        )

        return render_template('result.html',
                               calories=int(final_calories),
                               protein=protein,
                               fats=fats,
                               carbs=carbs,
                               meals=selected_items,
                               total_cal=int(total_cal),
                               total_protein=round(total_protein),
                               total_carbs=round(total_carbs),
                               total_fat=round(total_fat),
                               goal=goal)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
