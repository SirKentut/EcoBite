from google import genai
from dotenv import load_dotenv
import os
import re
import requests
import json

class Predictor:

    client = None
    image_path = None

    def __init__(self, image_path):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
        self.image_path = image_path

    def get_foods(self):
        file = self.client.files.upload(file=self.image_path)
        prompt = ("You are given an image of some food that may be uneaten or partially eaten. "
                  "Your task is to figure out all the different foods in the image and name them in JSON format. "
                  "The JSON should have one key called 'foods' that holds an array of food names (strings). "
                  "Show your thought process, and when you're done, wrap the JSON output in a JSON html tag. For parsing purposes, only include the JSON html tag in your response when you are returning the JSON."
                  "To figure out the foods, follow these steps:\n"
                  "1. Isolate the foods if multiple foods exist in the image."
                  "2. Use your knowledge base to categorize each food\n"
                  "Here is an example JSON output that I expect from you: \n"
                  "<json>{foods: ['apple', 'orange', 'chicken']}</json>")
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=[prompt, file])
        foods = self.parse_food_json(response.text)
        return foods

    def get_volume(self, foods):
        file = self.client.files.upload(file=self.image_path)
        prompt2 = ("You are given an image of some food that may be uneaten or partially eaten. "
                   "Your task is to figure out the volume of the foods (in Liters) in the image and output them in JSON format. "
                   "Your JSON response should have a key for each food and the value of each key should be the volume of that food (as a float). "
                   "The foods in the images are: " + foods + "\n\n"
                   "Rules to follow in your response:\n"
                   "1. Show your thought process\n"
                   "2. Put your JSON response in a <json> tag. "
                   "There should only be one opening 'json' HTML tag and one closing 'json' HTML tag in your response. This is to be used when you are constructing your JSON response.\n\n"
                   "Here is an example JSON output that I expect from you:\n"
                   "<json>{\"rice\": 0.25, \"fried tofu\": 0.33, \"fried garlic\": 0.03}</json>")
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt2, file])
        # print("VOLUME RESPONSE")
        # print(response.text)
        map = parse_volume_json(response.text)
        return response.text, map

    def get_weight(self, food_map):
        prompt2 = ("You are given this JSON string representing a dish where each key is a food and its value is its volume:\n\n"
                   f"{food_map}\n\n"
                   "Given the volume of the food, find its density by multiplying it, "
                   "mathematically not programmatically, by its volume"
                   " (volume is given in the JSON string in Liters) to get the weight of the food. "
                   "Output your solution as a JSON formatted string where each key is the food and its value is"
                   " the weight (as a float in grams). \n\n"
                   "Rules to follow in your response:\n"
                   "1. Show your thought process\n"
                   "2. Put your JSON response in a <json> tag. "
                   "There should only be one opening 'json' HTML tag and one closing 'json' HTML"
                   " tag in your response. This is to be used when you are constructing your"
                   " JSON response.\n\n"
                   "Here is an example JSON output that I expect from you:\n"
                   "<json>{\"rice\": 100, \"fried tofu\": 120, \"fried garlic\": 80}</json>")
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=[prompt2])
        # print("WEIGHT RESPONSE")
        # print(response.text)
        map = parse_volume_json(response.text)
        return response.text, map

    def download_image(self):
        img_data = requests.get(self.image_path).content
        with open(self.image_path+'.jpg', 'wb') as handler:
            handler.write(img_data)

    def parse_food_json(self, input_string):
        # Regular expression to find the content inside <json> tags
        json_pattern = re.compile(r'<json>(.*?)</json>', re.DOTALL)

        # Search for the JSON content within the <json> tags
        match = json_pattern.search(input_string)

        if not match:
            raise ValueError("No <json> tag found in the input string.")

        json_content = match.group(1).strip()

        try:
            # Parse the JSON content
            parsed_json = json.loads(json_content)

            # Assuming the JSON contains only one key which maps to an array
            if not isinstance(parsed_json, dict) or len(parsed_json) != 1:
                raise ValueError("The JSON should contain exactly one key mapping to an array.")

            # Extract the array from the JSON
            array = next(iter(parsed_json.values()))

            if not isinstance(array, list):
                raise ValueError("The value associated with the key should be an array.")

            regular_string = ', '.join(array)
            return regular_string

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON content: {e}")


def parse_volume_json(input_string):
    # Regular expression to find the content inside <json> tags
    json_pattern = re.compile(r'<json>(.*?)</json>', re.DOTALL)

    # Search for the JSON content within the <json> tags
    match = json_pattern.search(input_string)

    if not match:
        raise ValueError("No <json> tag found in the input string.")

    json_content = match.group(1).strip()

    try:
        # Parse the JSON content
        parsed_json = json.loads(json_content)

        # Ensure the parsed JSON is a dictionary
        if not isinstance(parsed_json, dict):
            raise ValueError("The JSON content must be a dictionary.")

        # Validate that all values are integers
        for key, value in parsed_json.items():
            if not isinstance(value, float):
                raise ValueError(f"The value for key '{key}' is not an float.")

        # Return the dictionary
        return parsed_json

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON content: {e}")