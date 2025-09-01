# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CascadeLearning is a full-stack application that implements an intelligent cascade learning system for AI query routing. The system automatically routes queries to the most cost-effective AI model (tiny → medium → large) while maintaining response quality, achieving up to 70% cost savings.

## Architecture

### Backend (FastAPI + Python)
- **FastAPI Server** (`backend/main.py`): Main application with CORS, query processing, and statistics endpoints
- **Cascade Router** (`backend/router.py`): Intelligent routing logic that analyzes query complexity and selects appropriate model size
- **Model Client** (`backend/models.py`): Handles Hugging Face API integration for three model sizes (Tiny: Phi-2, Medium: Mistral-7B, Large: Llama-3-8B)
- **Database Layer** (`backend/database.py`): SQLAlchemy models for query logging and cost tracking
- **Configuration** (`backend/config.py`): Pydantic settings with environment variable support

### Frontend (Next.js + TypeScript)
- **Next.js 15** with TypeScript and Tailwind CSS v4
- **App Router** structure with components in `frontend/components/`
- **Query Interface** (`frontend/components/QueryInterface.tsx`): Main user interaction component
- **Metrics Display** (`frontend/components/MetricCard.tsx`): Real-time cost and performance metrics

### Key Features
- **Smart Query Routing**: Analyzes complexity, domain (code/math/general), and patterns to select optimal model
- **Automatic Escalation**: Falls back to larger models if confidence is low or response quality is poor  
- **Cost Tracking**: Real-time cost comparison against baseline (large model) with savings calculation
- **Query Caching**: MD5-based caching for routing decisions
- **Comprehensive Logging**: SQLite database with query logs and cost savings tracking

## Development Commands

### Backend Development
```bash
cd backend
# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# Install dependencies
pip install -r requirements.txt
# Run development server
python main.py
```

### Frontend Development  
```bash
cd frontend
# Install dependencies
npm install
# Run development server
npm run dev
# Build for production
npm run build
# Start production server
npm start
# Run linter
npm run lint
```

## Environment Setup

Create `.env` file in root directory with:
```
HUGGINGFACE_API_KEY=your_hf_api_key_here
DATABASE_URL=sqlite:///./cascade.db
```

## Database Schema

- **QueryLog**: Stores query hash, text, model used, response time, tokens, cost, confidence, routing reason, escalation status
- **CostSaving**: Tracks actual vs baseline costs and savings for each query

## Model Configuration

Three model tiers with different cost/capability trade-offs:
- **Tiny** (Phi-2): 2.7B params, $0.0001/1K tokens, 10s timeout - for simple queries
- **Medium** (Mistral-7B): 7B params, $0.0005/1K tokens, 15s timeout - for moderate/code queries  
- **Large** (Llama-3-8B): 8B params, $0.001/1K tokens, 20s timeout - for complex queries

## Testing

Backend test stubs exist in `backend/test_modules.py` and `backend/test_setup.py` but are not fully implemented yet.

## API Endpoints

- `GET /`: Service status and available endpoints
- `POST /query`: Main query processing with automatic routing
- `GET /stats`: Aggregate statistics (costs, savings, model distribution)  
- `GET /models`: Available model information
- `GET /health`: Health check
- `POST /demo`: Run predefined demo queries