from flask import Blueprint, jsonify, request
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create blueprint for density service
density = Blueprint('density', __name__)

# Initialize Perplexity client
client = OpenAI(
    api_key=os.getenv('PERPLEXITY_API_KEY'),
    base_url="https://api.perplexity.ai"
)

def get_density(food_name):
    """Query Perplexity API for food density."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a precise scientific assistant. When asked about food density, "
                "respond only with the numerical value in g/ml. If uncertain, respond with your best estimation."
            ),
        },
        {
            "role": "user",
            "content": f"What is the density of {food_name} in g/ml? Give me only the number and that is it."
        },
    ]
    
    try:
        response = client.chat.completions.create(
            model="sonar",
            messages=messages,
        )
        
        # Extract the density value
        density_str = response.choices[0].message.content.strip()
        try:
            density = float(density_str)
            print(f"Successful Perplexity Query: [Food Name: {food_name}, Density: {density}]")
            return density
        except ValueError:
            print(f"Error: Could not convert density value '{density_str}' to float for {food_name}")
            return None
            
    except Exception as e:
        print(f"Error getting density for {food_name}: {str(e)}")
        return None

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
        if not isinstance(food, dict) or 'name' not in food:
            continue
            
        # Get the density for the food using Perplexity Search    
        density_value = get_density(food['name'])
        
        processed_foods.append({
            "food_name": food['name'],
            "density": density_value
        })
    
    return jsonify({
        'foods': processed_foods
    })