# EcoBite Flask Service

## Getting Started

1. Make sure you have Python 3.8 or higher installed

2. Navigate to the flask directory:
```bash
cd flask
```

3. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. Install required packages:
```bash
pip install flask pandas openai python-dotenv
```

5. Create a `.env` file with your API key:
```
PERPLEXITY_API_KEY=your_api_key_here
```

6. Start the Flask server:
```bash
python app.py
```

The server will start on port 5000. You can verify it's running by accessing:
http://localhost:5000/health