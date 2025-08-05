# backend/models.py
from enum import Enum
from typing import Dict, Any, Union
import httpx
from config import settings

class ModelSize(Enum):
    TINY = "tiny"
    MEDIUM = "medium"
    LARGE = "large"

MODEL_CONFIGS = {
    ModelSize.TINY: {
        "id": "microsoft/phi-2",
        "name": "Phi-2",
        "params": "2.7B",
        "cost_per_token": 0.0000001,  # $0.0001 per 1K tokens
        "max_tokens": 2048,
        "timeout": 10
    },
    ModelSize.MEDIUM: {
        "id": "mistralai/Mistral-7B-Instruct-v0.2",
        "name": "Mistral-7B",
        "params": "7B",
        "cost_per_token": 0.0000005,  # $0.0005 per 1K tokens
        "max_tokens": 4096,
        "timeout": 15
    },
    ModelSize.LARGE: {
        "id": "meta-llama/Meta-Llama-3-8B-Instruct",
        "name": "Llama-3-8B",
        "params": "8B",
        "cost_per_token": 0.000001,  # $0.001 per 1K tokens
        "max_tokens": 8192,
        "timeout": 20
    }
}

class ModelClient:
    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.base_url = "https://api-inference.huggingface.co/models"
        
    async def query_model(self, model_size: ModelSize, prompt: str) -> Dict[str, Any]:
        """Query a specific model via Hugging Face Inference API"""
        config = MODEL_CONFIGS[model_size]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": min(256, config["max_tokens"]),
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/{config['id']}",
                    json=payload,
                    headers=headers,
                    timeout=config["timeout"]
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    text = result.get("generated_text", "")
                else:
                    text = ""
                
                # Calculate tokens (rough estimate)
                tokens = len(text.split()) * 1.3
                cost = tokens * config["cost_per_token"]
                
                return {
                    "text": text,
                    "model": config["name"],
                    "tokens": int(tokens),
                    "cost": cost,
                    "model_size": model_size.value
                }
                
            except httpx.HTTPError as e:
                print(f"Error querying {config['name']}: {e}")
                # Fallback to next size up
                if model_size == ModelSize.TINY:
                    print("Falling back to MEDIUM model...")
                    return await self.query_model(ModelSize.MEDIUM, prompt)
                elif model_size == ModelSize.MEDIUM:
                    print("Falling back to LARGE model...")
                    return await self.query_model(ModelSize.LARGE, prompt)
                else:
                    # No more fallbacks available
                    return {
                        "text": f"Error: All models failed. Last error: {str(e)}",
                        "model": config["name"],
                        "tokens": 0,
                        "cost": 0,
                        "model_size": model_size.value,
                        "error": True
                    }