# Diet Planner Web Application

A Flask-based web app that generates personalized diet plans based on your age, gender, height, weight, activity level, and fitness goals (weight loss, maintenance, or gain). The app uses a simple machine learning model to suggest meals that fit your nutritional requirements.

---

## Features

- Calculates your Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) based on user input.
- Adjusts daily calorie needs according to your activity level and weight goal.
- Computes macronutrient targets (protein, fats, carbs) from calorie requirements.
- Uses a basic Decision Tree Classifier to recommend meals aligned with your fitness goal.
- Responsive, user-friendly interface with modern CSS styling.
- Shows a detailed nutrition summary and meal suggestions on the result page.

---

## How Machine Learning is Used

This app incorporates a basic **Decision Tree Classifier** from the `scikit-learn` library to predict which foods best match your fitness goal (weight loss, maintain, or weight gain). Here’s how it works:

- A small dataset of food items with nutritional values (calories, protein, fat, carbs) and their associated goals is used to train the model.
- The Decision Tree learns patterns from this data to classify foods according to different goals.
- When suggesting meals, the model predicts if a food fits your goal, helping the app select appropriate meals while respecting your calorie and macronutrient limits.

This simple ML approach adds adaptability to the diet plan, making recommendations smarter than fixed menus.

---

## Technologies Used

- Python 3
- Flask Web Framework
- scikit-learn (Decision Tree Classifier)
- HTML, CSS (with animations)
- Jinja2 templating

---



