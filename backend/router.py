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

class CascadeRouter:
    def __init__(self):
        # Keywords that indicate code-related queries
        self.code_keywords = [
            "code", "function", "debug", "error", "python", "javascript",
            "java", "cpp", "sql", "api", "class", "method", "variable",
            "loop", "array", "algorithm", "implement", "syntax"
        ]
        
        # Keywords that indicate complex queries
        self.complex_keywords = [
            "explain", "analyze", "compare", "evaluate", "design",
            "architect", "strategy", "comprehensive", "detailed",
            "step-by-step", "pros and cons", "trade-offs"
        ]
        
        # Simple query patterns
        self.simple_patterns = [
            r"^what is .*\?$",
            r"^who is .*\?$",
            r"^when .*\?$",
            r"^where .*\?$",
            r"^how many .*\?$",
            r"^yes or no.*\?$",
            r"^true or false.*\?$"
        ]
        
        # Cache for recent routing decisions
        self.decision_cache: Dict[str, RouteDecision] = {}
        
    def analyze_complexity(self, query: str) -> QueryComplexity:
        """Analyze query complexity based on multiple factors"""
        query_lower = query.lower()
        
        # Factor 1: Query length
        word_count = len(query.split())
        
        # Factor 2: Check for simple patterns
        for pattern in self.simple_patterns:
            if re.match(pattern, query_lower):
                return QueryComplexity.SIMPLE
        
        # Factor 3: Check for complex keywords
        complex_score = sum(1 for keyword in self.complex_keywords 
                          if keyword in query_lower)
        
        # Factor 4: Question depth (number of questions)
        question_count = query.count('?')
        
        # Factor 5: Technical complexity
        technical_score = sum(1 for keyword in self.code_keywords 
                            if keyword in query_lower)
        
        # Scoring logic
        if word_count < 10 and complex_score == 0:
            return QueryComplexity.SIMPLE
        elif word_count > 50 or complex_score >= 2 or question_count > 2:
            return QueryComplexity.COMPLEX
        else:
            return QueryComplexity.MODERATE
            
    