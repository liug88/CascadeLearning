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
            
    def detect_domain(self, query: str) -> str:
        """Detect the domain of the query"""
        query_lower = query.lower()
        
        # Check for code domain
        code_score = sum(1 for keyword in self.code_keywords 
                        if keyword in query_lower)
        if code_score >= 2:
            return "code"
            
        # Check for math domain
        math_keywords = ["calculate", "solve", "equation", "math", "number"]
        math_score = sum(1 for keyword in math_keywords 
                        if keyword in query_lower)
        if math_score >= 2:
            return "math"
            
        return "general"
    
    def calculate_confidence(self, query: str, model_size: ModelSize) -> float:
        """Calculate confidence score for routing decision"""
        complexity = self.analyze_complexity(query)
        
        # Confidence matrix based on complexity and model size
        confidence_matrix = {
            (QueryComplexity.SIMPLE, ModelSize.TINY): 0.95,
            (QueryComplexity.SIMPLE, ModelSize.MEDIUM): 0.98,
            (QueryComplexity.SIMPLE, ModelSize.LARGE): 0.99,
            
            (QueryComplexity.MODERATE, ModelSize.TINY): 0.60,
            (QueryComplexity.MODERATE, ModelSize.MEDIUM): 0.90,
            (QueryComplexity.MODERATE, ModelSize.LARGE): 0.95,
            
            (QueryComplexity.COMPLEX, ModelSize.TINY): 0.30,
            (QueryComplexity.COMPLEX, ModelSize.MEDIUM): 0.70,
            (QueryComplexity.COMPLEX, ModelSize.LARGE): 0.95,
        }
        
        return confidence_matrix.get((complexity, model_size), 0.5)
    
    def get_query_hash(self, query: str) -> str:
        """Generate hash for query caching"""
        return hashlib.md5(query.encode()).hexdigest()
    
    def route(self, query: str) -> RouteDecision:
        """Main routing logic"""
        # Check cache first
        query_hash = self.get_query_hash(query)
        if query_hash in self.decision_cache:
            return self.decision_cache[query_hash]
        
        # Analyze query
        complexity = self.analyze_complexity(query)
        domain = self.detect_domain(query)
        
        # Routing logic
        if complexity == QueryComplexity.SIMPLE:
            model_size = ModelSize.TINY
            reason = "Simple query - using tiny model for efficiency"
            
        elif complexity == QueryComplexity.MODERATE:
            if domain == "code":
                model_size = ModelSize.MEDIUM
                reason = "Code-related query - using medium model"
            else:
                model_size = ModelSize.TINY
                reason = "Moderate query - attempting tiny model first"
                
        else:  # COMPLEX
            if domain == "code":
                model_size = ModelSize.LARGE
                reason = "Complex code query - using large model"
            else:
                model_size = ModelSize.MEDIUM
                reason = "Complex query - using medium model"
        
        confidence = self.calculate_confidence(query, model_size)
        decision = RouteDecision(model_size, confidence, reason)
        
        # Cache decision
        self.decision_cache[query_hash] = decision
        
        return decision
    
    def should_escalate(self, response: str, confidence: float) -> bool:
        """Determine if we should escalate to a larger model"""
        # Check for obvious failure indicators
        failure_indicators = [
            "i cannot", "i don't understand", "unclear", "error",
            "sorry", "unable to"
        ]
        
        response_lower = response.lower()
        has_failure = any(indicator in response_lower 
                         for indicator in failure_indicators)
        
        # Check response length (too short might indicate failure)
        is_too_short = len(response.split()) < 10
        
        # Escalate if confidence is low OR response seems inadequate
        return confidence < 0.7 or has_failure or is_too_short