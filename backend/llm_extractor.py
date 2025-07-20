from groq import Groq
import json
import os
from typing import Dict, Union
from dotenv import load_dotenv
import os

# Load from .env in project root
load_dotenv()  

client = Groq(api_key=os.getenv("GROQ_API_KEY"))



def extract_lab_data(text: str) -> Dict[str, Union[float, str]]:
    """
    Extract wine lab data using Groq's Llama 3.1 model
    Returns dict with extracted values or error message
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """You are a wine lab data extraction specialist. 
                    Extract the following values as JSON with float numbers only:
                    fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
                    chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density,
                    pH, sulphates, alcohol"""
                },
                {
                    "role": "user",
                    "content": f"""Extract the wine measurements from this text as JSON.
                    Example Output:
                    {{
                        "fixed_acidity": 7.4,
                        "volatile_acidity": 0.7,
                        ...
                    }}
                    
                    Text to analyze:
                    {text}"""
                }
            ],
            temperature=0.1,
            max_tokens=300,
            response_format={"type": "json_object"}
        )

        # Parse and validate the response
        result = json.loads(response.choices[0].message.content)
        
        # Convert all values to float
        for key in result:
            try:
                result[key] = float(result[key])
            except (ValueError, TypeError):
                result[key] = 0.0  # Default value if conversion fails
        
        return result

    except Exception as e:
        return {"error": f"Extraction failed: {str(e)}"}