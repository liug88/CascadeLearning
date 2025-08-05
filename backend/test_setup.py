"""
Test script to verify all dependencies are working correctly
"""

def test_imports():
    """Test all package imports"""
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
        
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        import pydantic
        print("✅ Pydantic imported successfully")
        
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
        
        import httpx
        print("✅ HTTPX imported successfully")
        
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
        
        import jose
        print("✅ Python-jose imported successfully")
        
        print("\n🎉 All dependencies imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI app creation"""
    try:
        from main import app
        print("✅ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI app error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Cascade Learning Backend Dependencies\n")
    print("=" * 50)
    
    imports_ok = test_imports()
    app_ok = test_fastapi_app()
    
    print("\n" + "=" * 50)
    if imports_ok and app_ok:
        print("🎉 All tests passed! Your backend is ready to go!")
    else:
        print("❌ Some tests failed. Check the errors above.")
