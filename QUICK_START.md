# Quick Start Guide

Get the AI Commerce Agent running in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ and npm installed
- Git installed

## Installation

### Option 1: Automated Script (Recommended)

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
cd backend
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

Backend will start on `http://localhost:8000`

#### 2. Frontend Setup (in a new terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend will start on `http://localhost:3000`

## Usage

### Opening the Application

1. Open your browser to `http://localhost:3000`
2. You'll see the ShopAssist chat interface

### Testing the Features

#### 1. General Conversation

Try asking:
- "What's your name?"
- "What can you do?"
- "Hello"

#### 2. Text-Based Recommendations

Try asking:
- "Recommend me a t-shirt for sports"
- "Show me running shoes"
- "I need a yoga mat"

#### 3. Image-Based Search

1. Click the camera icon 📷
2. Upload any image
3. Get product recommendations

## API Documentation

While backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Common Issues

**Backend won't start:**
- Make sure Python 3.9+ is installed
- Check port 8000 is not in use

**Frontend won't start:**
- Make sure Node.js 18+ is installed
- Check port 3000 is not in use
- Run `npm install` again

**API connection errors:**
- Verify backend is running on port 8000
- Check browser console for errors
- Make sure CORS is enabled (it is by default)

## Next Steps

- Read [README.md](README.md) for full documentation
- Read [DEPLOYMENT.md](DEPLOYMENT.md) to deploy to production
- Customize products in `backend/database.py`
- Add your own features!

## Support

If you encounter issues:
1. Check the terminal for error messages
2. Check browser console (F12)
3. Verify all dependencies are installed
4. Try restarting both servers

---

**Happy Coding! 🎉**

