# Cascade Learning Platform

An intelligent AI query routing system that automatically selects the most cost-effective AI model (tiny → medium → large) while maintaining response quality, achieving up to 70% cost savings.

## 🌟 Features

- **🎯 Smart Query Routing**: Analyzes query complexity and domain to select optimal model
- **💰 Cost Optimization**: Reduces AI costs by up to 70% compared to using large models for everything
- **⚡ Automatic Escalation**: Falls back to larger models if confidence is low or response quality is poor
- **📊 Real-time Analytics**: Track costs, savings, response times, and model usage distribution
- **🔄 Intelligent Caching**: MD5-based caching for routing decisions
- **📈 Comprehensive Logging**: SQLite database with detailed query logs and cost tracking

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **FastAPI Server** (`backend/main.py`): Main application with CORS, query processing, and statistics endpoints
- **Cascade Router** (`backend/router.py`): Intelligent routing logic that analyzes query complexity and selects appropriate model size  
- **Model Client** (`backend/models.py`): Handles Hugging Face API integration for three model sizes:
  - **Tiny** (Phi-2): 2.7B params, $0.0001/1K tokens - for simple queries
  - **Medium** (Mistral-7B): 7B params, $0.0005/1K tokens - for moderate/code queries
  - **Large** (Llama-3-8B): 8B params, $0.001/1K tokens - for complex queries
- **Database Layer** (`backend/database.py`): SQLAlchemy models for query logging and cost tracking
- **Configuration** (`backend/config.py`): Pydantic settings with environment variable support

### Frontend (Next.js + TypeScript)
- **Next.js 15** with TypeScript and Tailwind CSS v4
- **App Router** structure with modern React patterns
- **Query Interface**: Real-time query processing with loading states and error handling
- **Statistics Dashboard**: Interactive analytics with model usage distribution
- **Responsive Design**: Mobile-friendly interface with professional styling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Node.js 18+
- Hugging Face API key

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CascadeLearning
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file in root directory
# Add your Hugging Face API key:
echo "HUGGINGFACE_API_KEY=your_hf_api_key_here" > ../.env
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# The .env.local file is already configured for local development
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```
The API will be available at http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
The web application will be available at http://localhost:3000

## 📋 API Endpoints

- `GET /`: Service status and available endpoints
- `POST /query`: Main query processing with automatic routing
- `GET /stats`: Aggregate statistics (costs, savings, model distribution)
- `GET /models`: Available model information
- `GET /health`: Health check endpoint
- `POST /demo`: Run predefined demo queries

## 🧪 Testing

### Try Sample Queries
- **Simple**: "What is 2+2?"
- **Moderate**: "Explain recursion in programming"  
- **Complex**: "Write a Python function to implement a binary search tree with insertion and deletion methods"
- **Code-focused**: "Debug this Python code: [paste code]"

### Run Demo
Click the "Run Demo" button in the statistics dashboard to automatically process predefined queries and see the system in action.

## 📊 Model Selection Logic

The cascade router analyzes queries based on:
- **Query Length**: Word count and complexity indicators
- **Domain Detection**: Code, math, or general queries
- **Pattern Matching**: Simple question patterns (what/who/when/where)
- **Keyword Analysis**: Technical terms and complexity markers
- **Confidence Scoring**: Probability of successful response

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm run dev          # Development server
npm run build        # Production build
npm run start        # Production server
npm run lint         # ESLint
```

### Backend Development
```bash
cd backend
python main.py       # Run FastAPI server
# Tests coming soon - stubs in test_modules.py
```

### Environment Variables

**Root `.env`:**
```
HUGGINGFACE_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./cascade.db
CORS_ORIGINS=["http://localhost:3000"]
PORT=8000
```

**Frontend `.env.local`:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using type hints
- **Uvicorn**: ASGI server
- **httpx**: Async HTTP client for API calls

### Frontend  
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type safety
- **Tailwind CSS v4**: Utility-first styling
- **React Hooks**: Modern state management

## 📈 Performance Metrics

The system tracks and displays:
- Total queries processed
- Actual costs vs baseline (large model) costs
- Percentage savings achieved
- Average response times
- Model usage distribution
- Query success rates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd CascadeLearning

# Create environment file
echo "HUGGINGFACE_API_KEY=your_hf_api_key_here" > .env

# Start all services
docker-compose up --build

# Visit http://localhost:3000
```

### Manual Docker Deployment

**Backend:**
```bash
cd backend
docker build -t cascade-backend .
docker run -p 8000:8000 -e HUGGINGFACE_API_KEY=your_key cascade-backend
```

**Frontend:**
```bash
cd frontend
docker build -t cascade-frontend .
docker run -p 3000:3000 cascade-frontend
```

## 🚀 Production Deployment

### Environment Variables for Production

```bash
# Backend (.env)
HUGGINGFACE_API_KEY=your_production_key
DATABASE_URL=sqlite:///./data/cascade.db
CORS_ORIGINS=["https://your-domain.com"]
PORT=8000

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://api.your-domain.com
```

### Recommended Hosting

- **Frontend**: Vercel, Netlify, or AWS S3 + CloudFront
- **Backend**: Railway, Heroku, DigitalOcean, or AWS ECS
- **Database**: For production, consider PostgreSQL or MongoDB

## 🎯 Roadmap

- [ ] Add more model providers (OpenAI, Anthropic, etc.)
- [ ] Implement user authentication and query history
- [ ] Add batch processing capabilities
- [x] Create Docker deployment configuration
- [ ] Add comprehensive test suite
- [ ] Implement advanced routing strategies
- [ ] Add cost budgeting and alerts
- [ ] Add PostgreSQL support
- [ ] Implement caching with Redis
- [ ] Add monitoring and observability
