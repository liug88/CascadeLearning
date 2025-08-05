# Cascade Learning Project

A full-stack application for implementing cascade learning algorithms with a Python backend and Next.js frontend.

## Project Structure

```
CascadeLearning/
├── backend/          # Python FastAPI backend
│   ├── venv/         # Python virtual environment
│   ├── main.py       # FastAPI application entry point
│   ├── router.py     # API routes
│   ├── models.py     # Data models
│   ├── database.py   # Database configuration
│   ├── config.py     # Application configuration
│   └── requirements.txt
├── frontend/         # Next.js React frontend
├── data/            # Data storage and processing
├── docs/            # Documentation
├── .env             # Environment variables
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```powershell
   cd backend
   ```

2. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```powershell
   python main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```powershell
   cd frontend
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Run the development server:
   ```powershell
   npm run dev
   ```

## Features

- **Backend**: FastAPI with SQLAlchemy for database operations
- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **Machine Learning**: Cascade learning implementation with scikit-learn and PyTorch
- **Data Processing**: Pandas and NumPy for data manipulation
- **Visualization**: Matplotlib and Seaborn for data visualization

## Development

The project is set up with:
- Python virtual environment for backend dependencies
- Node.js packages managed with npm
- Git for version control
- Environment variables for configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
