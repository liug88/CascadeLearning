# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import time
from datetime import datetime, timezone

from config import settings
from router import CascadeRouter
from models import ModelClient, ModelSize, MODEL_CONFIGS
from database import get_db, log_query, log_savings, get_stats

app = FastAPI(title="CascadeLearn API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
router = CascadeRouter()
model_client = ModelClient()

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    force_model: Optional[str] = None  # For testing specific models

class QueryResponse(BaseModel):
    response: str
    model_used: str
    model_size: str
    tokens: int
    cost: float
    savings: float
    response_time: float
    confidence: float
    routing_reason: str

class StatsResponse(BaseModel):
    total_queries: int
    total_cost: float
    total_saved: float
    avg_response_time: float
    model_distribution: Dict[str, int]
    savings_percentage: float

@app.get("/")
async def root():
    return {
        "name": "CascadeLearn API",
        "status": "running",
        "endpoints": ["/query", "/stats", "/models", "/health"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

@app.get("/models")
async def get_models():
    """Get information about available models"""
    return {
        model_size.value: {
            "name": config["name"],
            "parameters": config["params"],
            "cost_per_1k_tokens": config["cost_per_token"] * 1000
        }
        for model_size, config in MODEL_CONFIGS.items()
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest, db=Depends(get_db)):
    """Process a query through the cascade router"""
    start_time = time.time()
    
    try:
        # Route the query
        if request.force_model:
            # Allow forcing a specific model for testing
            model_size = ModelSize(request.force_model)
            # Create a simple routing decision object
            from dataclasses import dataclass
            
            @dataclass
            class RouteDecision:
                model_size: ModelSize
                confidence: float
                reason: str
            
            routing_decision = RouteDecision(
                model_size, 1.0, "Forced model selection"
            )
        else:
            routing_decision = router.route(request.query)
        
        # Query the selected model
        result = await model_client.query_model(
            routing_decision.model_size,
            request.query
        )
        
        # Check if we need to escalate
        if router.should_escalate(result["text"], routing_decision.confidence):
            # Try the next larger model
            if routing_decision.model_size == ModelSize.TINY:
                new_size = ModelSize.MEDIUM
            elif routing_decision.model_size == ModelSize.MEDIUM:
                new_size = ModelSize.LARGE
            else:
                new_size = ModelSize.LARGE
            
            result = await model_client.query_model(new_size, request.query)
            was_escalated = True
        else:
            was_escalated = False
        
        response_time = time.time() - start_time
        
        # Calculate savings (compare to large model)
        baseline_cost = (result["tokens"] * 
                        MODEL_CONFIGS[ModelSize.LARGE]["cost_per_token"])
        actual_cost = result["cost"]
        savings = baseline_cost - actual_cost
        
        # Log to database
        log_query(db, {
            "query_hash": router.get_query_hash(request.query),
            "query_text": request.query[:500],  # Truncate long queries
            "model_used": result["model"],
            "model_size": result["model_size"],
            "response_time": response_time,
            "tokens_used": result["tokens"],
            "cost": actual_cost,
            "confidence": routing_decision.confidence,
            "routing_reason": routing_decision.reason,
            "was_escalated": int(was_escalated)
        })
        
        log_savings(db, {
            "query_hash": router.get_query_hash(request.query),
            "actual_cost": actual_cost,
            "baseline_cost": baseline_cost,
            "saved": savings
        })
        
        return QueryResponse(
            response=result["text"],
            model_used=result["model"],
            model_size=result["model_size"],
            tokens=result["tokens"],
            cost=actual_cost,
            savings=savings,
            response_time=response_time,
            confidence=routing_decision.confidence,
            routing_reason=routing_decision.reason
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=StatsResponse)
async def get_statistics(db=Depends(get_db)):
    """Get aggregate statistics"""
    stats = get_stats(db)
    
    # Calculate savings percentage
    if stats["total_cost"] > 0:
        total_baseline = stats["total_cost"] + stats["total_saved"]
        savings_percentage = (stats["total_saved"] / total_baseline) * 100
    else:
        savings_percentage = 0
    
    stats["savings_percentage"] = round(savings_percentage, 2)
    
    return StatsResponse(**stats)

@app.post("/demo")
async def run_demo(db=Depends(get_db)):
    """Run a demo with predefined queries"""
    demo_queries = [
        "What is 2+2?",
        "Explain the concept of recursion in programming",
        "Write a Python function to calculate fibonacci numbers",
        "What's the capital of France?",
        "Analyze the pros and cons of microservices architecture",
    ]
    
    results = []
    for query in demo_queries:
        response = await process_query(QueryRequest(query=query), db)
        results.append({
            "query": query,
            "model": response.model_used,
            "cost": response.cost,
            "savings": response.savings,
            "time": response.response_time
        })
    
    return {"demo_results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)