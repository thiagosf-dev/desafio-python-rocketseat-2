from flask import Flask, jsonify, request
from database import db
from models.meal import Meal
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'api_secret_key'
db.init_app(app)


@app.route('/meals', methods=['POST'])
def create_meal():
    data = request.json
    name = data.get('name')
    if name:
        new_meal = Meal(
            name=name,
            description=data.get('description', ''),
            date_time=datetime.now(),
            is_within_diet=data.get('is_within_diet')
        )
        db.session.add(new_meal)
        db.session.commit()
        return jsonify({'message': 'Meal created successfully!', 'meal': {
            'id': new_meal.id,
            'name': new_meal.name,
            'description': new_meal.description,
            'date_time': new_meal.date_time.isoformat(),
            'is_within_diet': new_meal.is_within_diet
        }}), 201
    return jsonify({'message': 'Invalid data.'}), 400


@app.route('/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    data = request.json
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    meal.name = data['name']
    meal.description = data.get('description', meal.description)
    meal.date_time = datetime.now()
    meal.is_within_diet = data['is_within_diet']
    db.session.commit()
    return jsonify({'message': 'Meal updated successfully!', 'meal': {
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'date_time': meal.date_time.isoformat(),
        'is_within_diet': meal.is_within_diet
    }}), 200


@app.route('/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    db.session.delete(meal)
    db.session.commit()
    return jsonify({'message': 'Meal deleted successfully!'}), 200


@app.route('/meals', methods=['GET'])
def list_meals():
    meals = Meal.query.all()
    return jsonify({'meals': [{
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'date_time': meal.date_time.isoformat(),
        'is_within_diet': meal.is_within_diet
    } for meal in meals]}), 200

# Endpoint para visualizar uma única refeição


@app.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    return jsonify({
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'date_time': meal.date_time.isoformat(),
        'is_within_diet': meal.is_within_diet
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
