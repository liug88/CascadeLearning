from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from config import settings

Base = declarative_base()

class QueryLog(Base):
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    query_hash = Column(String(32), index=True)
    query_text = Column(Text)
    model_used = Column(String(50))
    model_size = Column(String(20))
    response_time = Column(Float)
    tokens_used = Column(Integer)
    cost = Column(Float)
    confidence = Column(Float)
    routing_reason = Column(Text)
    was_escalated = Column(Integer, default=0)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
class CostSaving(Base):
    __tablename__ = "cost_savings"
    
    id = Column(Integer, primary_key=True, index=True)
    query_hash = Column(String(32))
    actual_cost = Column(Float)
    baseline_cost = Column(Float)  # What GPT-4 would cost
    saved = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Create engine and session
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Database helper functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_query(db, query_data: dict):
    """Log a query and its routing decision"""
    log_entry = QueryLog(**query_data)
    db.add(log_entry)
    db.commit()
    return log_entry

def log_savings(db, savings_data: dict):
    """Log cost savings"""
    savings_entry = CostSaving(**savings_data)
    db.add(savings_entry)
    db.commit()
    return savings_entry

def get_stats(db):
    """Get aggregate statistics"""
    from sqlalchemy import func
    
    total_queries = db.query(QueryLog).count()
    total_cost = db.query(func.sum(QueryLog.cost)).scalar() or 0
    total_saved = db.query(func.sum(CostSaving.saved)).scalar() or 0
    avg_response_time = db.query(func.avg(QueryLog.response_time)).scalar() or 0
    
    model_distribution = db.query(
        QueryLog.model_size,
        func.count(QueryLog.id)
    ).group_by(QueryLog.model_size).all()
    
    return {
        "total_queries": total_queries,
        "total_cost": round(total_cost, 4),
        "total_saved": round(total_saved, 4),
        "avg_response_time": round(avg_response_time, 2),
        "model_distribution": dict(model_distribution)
    }