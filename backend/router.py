# backend/router.py
import re
from enum import Enum
from typing import Dict, Any, List
import hashlib
from models import ModelSize

class QueryComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"

class RouteDecision:
    def __init__(self, model_size: ModelSize, confidence: float, reason: str):
        self.model_size = model_size
        self.confidence = confidence
        self.reason = reason

