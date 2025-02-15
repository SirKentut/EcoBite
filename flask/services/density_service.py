from flask import Blueprint, jsonify, request

# Create blueprint for density service
density = Blueprint('density', __name__)

@density.route('/process-foods', methods=['POST'])
def process_foods():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    # Validate the request contains a list of foods
    if not isinstance(data, dict) or 'foods' not in data:
        return jsonify({'error': 'Request must include a "foods" list'}), 400
    
    foods = data['foods']
    if not isinstance(foods, list):
        return jsonify({'error': 'Foods must be a list'}), 400
        
    # Process each food item
    processed_foods = []
    for food in foods:
        processed_foods.append({
            "food name": food['name'],
            "density": 1
        })
    
    return jsonify({
        'foods': processed_foods
    })